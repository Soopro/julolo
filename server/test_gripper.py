# coding=utf-8
from __future__ import absolute_import

import argparse

import gripper


parser = argparse.ArgumentParser(description='Options of starting gripper.')

parser.add_argument('-t', '--test',
                    dest='config',
                    action='store_const',
                    const='testing',
                    help='Manually start debug as testing config.')

parser.add_argument('-p', '--production',
                    dest='config',
                    action='store_const',
                    const='production',
                    help='Manually start debug as production config.')

args, unknown = parser.parse_known_args()


if __name__ == '__main__':
    gripper.run(args.config or 'default')
