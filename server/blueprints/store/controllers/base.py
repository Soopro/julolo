# coding=utf-8
from __future__ import absolute_import

from flask import current_app

from utils.response import output_json
from utils.request import get_args, get_param
from utils.misc import parse_int

from apiresps.validations import Struct


@output_json
def get_store():
    store = {
        'tips': 'http://news.xinhuanet.com/gangao/2016-02/27/128756028_14564769438121n.jpg',
    }
    return output_store(store)


# outputs
def output_store(store):
    return {
        'tips': store['tips']

    }
