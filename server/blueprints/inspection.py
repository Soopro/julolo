# coding=utf-8
from __future__ import absolute_import

from flask import g, request

from helpers.identity import get_current_user, get_current_store


def _verify_jwt():
    g.user = get_current_user()


def _verify_store():
    g.store = get_current_store()


def verify_access(open_api=[]):
    _verify_store()
    if request.endpoint in open_api:
        pass
    else:
        _verify_jwt()
