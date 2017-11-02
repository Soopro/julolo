# coding=utf-8
from __future__ import absolute_import

from application import create_app
import argparse

parser = argparse.ArgumentParser(description='Options of start server.')

parser.add_argument('-f', '--file',
                    dest='file_path',
                    action='store',
                    nargs='?',
                    type=str,
                    const=None,
                    help='Define file path.')


args, unknown = parser.parse_known_args()

app = create_app(args.server_mode or 'default')

if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=15800, host='0.0.0.0')
