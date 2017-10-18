# coding=utf-8
from __future__ import absolute_import

from flask import current_app

from utils.response import output_json
from utils.request import get_args, get_param
from utils.misc import parse_int

from apiresps.validations import Struct


@output_json
def list_tips():
    tips = [{
        'key': 'how-to-buy',
        'title': '怎么买',
        'src': 'http://news.xinhuanet.com/gangao/2016-02/27/128756028_14564769438121n.jpg',
    },
    {
        'key': 'how-search',
        'title': '怎么搜',
        'src': 'http://news.xinhuanet.com/gangao/2016-02/27/128756028_14564769438121n.jpg',
    }]
    return [output_tip(tip) for tip in tips]


# outputs
def output_tip(tip):
    return {
        'title': tip['title'],
        'src': tip['src']
    }
