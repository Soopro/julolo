# coding=utf-8
from __future__ import absolute_import

from flask import g, request

from helpers.identity import get_current_user


def _verify_jwt():
    g.user = get_current_user()


def verify_access(open_api=[]):
    if request.endpoint in open_api:
        pass
    else:
        _verify_jwt()
