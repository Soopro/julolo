# coding=utf-8
from __future__ import absolute_import

from flask import current_app

from utils.response import output_json
from utils.request import get_args, get_param
from utils.misc import parse_int

from apiresps.validations import Struct


@output_json
def list_promotions():
    return []


# outputs
def output_promotion(promo):
    return {
        'id': promo['_id'],
        'src': promo['src'],
        'title': promo['title'],
        'favorite_id': promo['favorite_id']
    }
