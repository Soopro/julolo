# coding=utf-8
from __future__ import absolute_import

from flask import current_app

from utils.response import output_json
from utils.request import get_args
from utils.model import make_paginator, attach_extend
from utils.misc import parse_int

from helpers.media import media_safe_src


@output_json
def list_shortcuts():
    paged = parse_int(get_args('paged'), 1, 1)
    perpage = parse_int(get_args('perpage'), 60, 1)

    shortcuts = current_app.mongodb.Shortcut.find_activated()
    p = make_paginator(shortcuts, paged, perpage)
    return attach_extend(
        [output_shortcut(shortcut) for shortcut in shortcuts],
        {'_more': p.has_next, '_count': p.count}
    )


@output_json
def get_shortcut(shortcut_slug):
    shortcut = current_app.mongodb.Shortcut.find_one_by_slug(shortcut_slug)
    return output_shortcut(shortcut)


# outputs
def output_shortcut(shortcut):
    return {
        'id': shortcut['_id'],
        'slug': shortcut['slug'],
        'path': shortcut['path'],
        'src': media_safe_src(shortcut['src']),
        'updated': shortcut['updated'],
        'creation': shortcut['creation']
    }
