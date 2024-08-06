#!/usr/bin/env python3
#
# Copyright (C) 2023-2024 Matthias Klumpp <matthias@tenstral.net>
#
# SPDX-License-Identifier: LGPL-3.0+


import os
import sys
import shutil
import subprocess
import requests
import zipfile
import stat
from argparse import ArgumentParser
from tempfile import NamedTemporaryFile


SYNTALOS_GIT_URL = 'https://github.com/syntalos/syntalos.git'
DOXYBOOK2_REL_URL = 'https://github.com/matusnovak/doxybook2/releases/download/v1.5.0/doxybook2-linux-amd64-v1.5.0.zip'


class SyWebBuilder:
    """Helper to build the Syntalos website."""

    def __init__(self, root_dir):
        self._root_dir = root_dir
        self._local_ws = os.path.join(self._root_dir, '_temp')

    def _copy_images(self, src, dst):
        for root, _, files in os.walk(src):
            for fname in files:
                if fname.endswith(('.png', '.svg')):
                    src_file_path = os.path.join(root, fname)
                    relative_path = os.path.relpath(root, src)
                    dst_dir_path = os.path.join(dst, relative_path)

                    if not os.path.exists(dst_dir_path):
                        os.makedirs(dst_dir_path)

                    dst_file_path = os.path.join(dst_dir_path, fname)
                    self._copy_file(src_file_path, dst_file_path)

    def _copy_file(self, src, dst):
        shutil.copy2(src, dst)

        src_short = src.replace(self._root_dir, '')
        dst_short = dst.replace(self._root_dir, '')
        print(f"Copied {src_short} to {dst_short}")

    def _get_doxybook2_path(self):
        """Find Doxybook2, download it if necessary."""

        db2_path = shutil.which('doxybook2')
        if db2_path:
            return db2_path

        db2_path = os.path.join(self._local_ws, 'bin', 'doxybook2')
        if os.path.exists(db2_path):
            return db2_path

        with NamedTemporaryFile(delete=False, suffix='.zip') as temp_zip:
            temp_zip_path = temp_zip.name

            response = requests.get(DOXYBOOK2_REL_URL, stream=True)
            response.raise_for_status()
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    temp_zip.write(chunk)

            with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
                # extract only the binary
                zip_ref.extract('bin/doxybook2', self._local_ws)
            st = os.stat(db2_path)
            os.chmod(db2_path, st.st_mode | stat.S_IEXEC)

        return db2_path

    def _make_apidocs(self):
        """Generate C++ documentation."""

        doxygen_exe = shutil.which('doxygen')
        if not doxygen_exe:
            raise RuntimeError('The `doxygen` executable is missing. Install it to continue.')
        doxybook2_exe = self._get_doxybook2_path()

        api_md_out_dir = os.path.join(self._root_dir, 'content', 'api')
        if os.path.exists(os.path.join(api_md_out_dir, 'classes', '_index.md')):
            print('• C++ API documentation was already generated.')
            return

        # run Doxygen
        print('➤ Running Doxygen...')
        sy_docs_dir = os.path.join(self._local_ws, 'syntalos-src', 'docs')
        subprocess.check_call([doxygen_exe], cwd=sy_docs_dir)

        # transform Doxygen data to Markdown
        print('➤ Running Doxybook2...')
        sy_docs_dir = os.path.join(self._local_ws, 'syntalos-src', 'docs')
        subprocess.check_call(
            [
                doxybook2_exe,
                '-i',
                os.path.join(sy_docs_dir, 'xml'),
                '-o',
                api_md_out_dir,
                '-c',
                os.path.join(sy_docs_dir, 'doxybook', 'config.json'),
                '-t',
                os.path.join(sy_docs_dir, 'doxybook', 'templates'),
            ],
            cwd=sy_docs_dir,
        )

    def _make_changesinfo(self):
        """Create the changes info file."""

        print('➤ Writing changes history document...')
        with open(os.path.join(self._local_ws, 'syntalos-src', 'NEWS.md'), 'r') as f:
            news_data = f.read()
        with open(os.path.join(self._root_dir, 'content', 'get', 'changes.md'), 'w') as f:
            f.write('---\ntitle: Version History\n---\n\n')
            f.write(news_data)

    def _prepare(self) -> bool:
        """Prepare website."""

        if not shutil.which('rst2html'):
            raise RuntimeError('The `rst2html` executable is missing. Install it to continue.')

        print('➤ Updating Syntalos source copy...')
        sysrc_dir = os.path.join(self._local_ws, 'syntalos-src')
        if os.path.exists(sysrc_dir):
            subprocess.check_call(['git', '-C', sysrc_dir, 'pull'])
        else:
            subprocess.check_call(['git', 'clone', '--depth=1', SYNTALOS_GIT_URL, sysrc_dir])

        # create C++ documentation
        self._make_apidocs()

        # create version history document
        self._make_changesinfo()

        # copy module icons & graphics
        print('➤ Copying assets...')
        self._copy_images(
            os.path.join(sysrc_dir, 'modules'),
            os.path.join(self._root_dir, 'static', 'images', 'modules-src'),
        )
        self._copy_images(
            os.path.join(sysrc_dir, 'data', 'modules'),
            os.path.join(self._root_dir, 'static', 'images', 'modules-src'),
        )

        # copy prebuilt HTML Python docs
        self._copy_file(
            os.path.join(sysrc_dir, 'docs', 'pysy_mlink_api_embed.html'),
            os.path.join(self._root_dir, 'content', 'docs', 'pysy_mlink_api_embed.fragment'),
        )

        return True

    def serve(self) -> bool:
        """Build the Syntalos website and display it."""

        if not self._prepare():
            return False

        subprocess.check_call(['hugo', 'serve'])

        return True

    def publish(self, base_url=None) -> bool:
        """Build the Syntalos website and display it."""

        if not self._prepare():
            return False

        cmd = ['hugo', '--gc', '--minify']
        if base_url:
            cmd.extend(['--baseURL', base_url])

        subprocess.check_call(cmd)

        return True


def run(script_dir):

    parser = ArgumentParser(description='Build the Syntalos documentation & website.')
    parser.add_argument('command', choices=['serve', 'publish'], help='Command to execute.')
    parser.add_argument('--base-url', default=None, help='Base URL for the publish command.')

    args = parser.parse_args()

    builder = SyWebBuilder(script_dir)
    if args.command == 'serve':
        if not builder.serve():
            return 1
    elif args.command == 'publish':
        if not builder.publish(args.base_url):
            return 1
    else:
        print('No command set! Use either "serve" or "publish".')
        return 4

    return 0


if __name__ == '__main__':
    thisfile = os.path.realpath(__file__)
    if not os.path.isabs(thisfile):
        thisfile = os.path.normpath(os.path.join(os.getcwd(), thisfile))
    thisdir = os.path.normpath(os.path.join(os.path.dirname(thisfile)))
    os.chdir(thisdir)

    sys.exit(run(thisdir))
