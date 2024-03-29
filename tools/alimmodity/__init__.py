# coding=utf-8
from __future__ import absolute_import
import argparse


__version_info__ = ('0', '5', '0')
__version__ = '.'.join(__version_info__)


def command_options():

    parser = argparse.ArgumentParser(
        description='Options of run Alimmodity.')

    parser.add_argument('-v', '--version',
                        dest='version',
                        action='store_const',
                        const=True,
                        help='Show current version.')

    parser.add_argument('-f', '--file',
                        dest='file_path',
                        action='store',
                        nargs='?',
                        type=str,
                        const=None,
                        help='Define the file path.')

    parser.add_argument('-p', '--policy',
                        dest='policy_path',
                        action='store',
                        nargs='?',
                        type=str,
                        default='policy.json',
                        help='Define policy file path (json).')

    parser.add_argument('--category',
                        dest='category_path',
                        action='store',
                        nargs='?',
                        type=str,
                        help='Convert category json for policy usage.')

    opts, unknown = parser.parse_known_args()

    return opts


def run():
    from .main import convert, format_category
    opts = command_options()
    if opts.version:
        print 'Alimmodity:', __version__
    elif opts.file_path:
        convert(file_path=opts.file_path,
                policy_path=opts.policy_path)
    elif opts.category_path:
        format_category(file_path=opts.category_path)
