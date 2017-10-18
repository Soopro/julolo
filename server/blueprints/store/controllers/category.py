# coding=utf-8
from __future__ import absolute_import

from flask import current_app

from utils.response import output_json
from utils.request import get_args, get_param
from utils.misc import parse_int

from apiresps.validations import Struct


@output_json
def list_categories():
    return []


@output_json
def get_cat_coupons():
    return []


# outputs
def output_category(category):
    return {
        'id': category['_id'],
    }
