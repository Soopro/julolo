# coding=utf-8
from __future__ import absolute_import

from flask import current_app

from utils.response import output_json
from utils.request import get_args, get_param
from utils.misc import parse_int

from apiresps.validations import Struct


@output_json
def list_categories():
    categories = [
        {
            '_id': '123',
            'src': 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg',
            'label': 'Testgy',
            'caption': u''
        },
        {
            '_id': '123',
            'src': 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg',
            'label': 'Testgy',
            'caption': u''
        },
        {
            '_id': '123',
            'src': 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg',
            'label': 'Testgy',
            'caption': u''
        },
        {
            '_id': '123',
            'src': 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg',
            'label': 'Testgy',
            'caption': u''
        },
        {
            '_id': '123',
            'src': 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg',
            'label': 'Testgy',
            'caption': u''
        },
        {
            '_id': '123',
            'src': 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg',
            'label': 'Testgy',
            'caption': u''
        },
        {
            '_id': '123',
            'src': 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg',
            'label': 'Testgy',
            'caption': u''
        },
    ]
    return [output_category(cat) for cat in categories]


@output_json
def get_cat_coupons():
    return []


# outputs
def output_category(category):
    return {
        'id': category['_id'],
        'label': category['label'],
        'caption': category['caption'],
        'src': category['src'],
    }
