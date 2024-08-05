#!/usr/bin/env python3
#
# Copyright (C) 2023-2024 Matthias Klumpp <matthias@tenstral.net>
#
# SPDX-License-Identifier: LGPL-3.0+


import os
import sys
import shutil
import subprocess
from argparse import ArgumentParser
from glob import glob


SYNTALOS_GIT_URL = 'https://github.com/syntalos/syntalos.git'


class SyWebBuilder:
    """Helper to build the Syntalos website."""

    def __init__(self, root_dir):
        self._root_dir = root_dir

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

    def _prepare(self) -> bool:
        """Prepare website."""

        if not shutil.which('rst2html'):
            raise RuntimeError('The `rst2html` executable is missing. Install it to continue.')

        sysrc_dir = os.path.join(self._root_dir, '_temp', 'syntalos-src')
        if os.path.exists(sysrc_dir):
            subprocess.check_call(['git', '-C', sysrc_dir, 'pull'])
        else:
            subprocess.check_call(['git', 'clone', '--depth=1', SYNTALOS_GIT_URL, sysrc_dir])

        # copy module icons & graphics
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
