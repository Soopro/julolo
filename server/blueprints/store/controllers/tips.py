# coding=utf-8
from __future__ import absolute_import

from flask import current_app

from utils.response import output_json

from helpers.media import media_safe_src


@output_json
def list_tips():
    tips = current_app.mongodb.Tip.find_activated()
    return [output_tip(tip) for tip in tips]


# outputs
def output_tip(tip):
    return {
        'title': tip['title'],
        'content': tip['content'],
        'src': media_safe_src(tip['src'])
    }
