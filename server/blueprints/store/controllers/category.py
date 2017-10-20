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
            'slug': 'test',
            'cat_ids': '18, 16',
            'src': 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg',
            'label': 'Fuck',
            'title': 'Fuck titasdlfdas ',
            'caption': u'哈哈，哈哈，哈哈'
        },
        {
            '_id': '123',
            'slug': 'test',
            'cat_ids': '18, 16',
            'src': 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg',
            'label': 'Testgy',
            'title': 'Fuck titasdlfdas ',
            'caption': u''
        },
        {
            '_id': '123',
            'slug': 'test',
            'cat_ids': '18, 16',
            'src': 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg',
            'label': 'Testgy',
            'title': 'Fuck titasdlfdas ',
            'caption': u''
        },
        {
            '_id': '123',
            'slug': 'test',
            'cat_ids': '18, 16',
            'src': 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg',
            'label': 'Testgy',
            'title': 'Fuck titasdlfdas ',
            'caption': u''
        },
        {
            '_id': '123',
            'slug': 'test',
            'cat_ids': '18, 16',
            'src': 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg',
            'label': 'Testgy',
            'title': 'Fuck titasdlfdas ',
            'caption': u''
        },
        {
            '_id': '123',
            'slug': 'test',
            'cat_ids': '18, 16',
            'src': 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg',
            'label': 'Testgy',
            'title': 'Fuck titasdlfdas ',
            'caption': u''
        },
        {
            '_id': '123',
            'slug': 'test',
            'cat_ids': '18, 16',
            'src': 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg',
            'label': 'Testgy',
            'title': 'Fuck titasdlfdas ',
            'caption': u''
        },
    ]
    return [output_category(cat) for cat in categories]


@output_json
def get_category(cat_slug):
    category = {
        '_id': '123',
        'slug': 'test',
        'cat_ids': '18, 16',
        'src': 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg',
        'label': 'Fuck',
        'title': 'Fuck titasdlfdas ',
        'caption': u''
    }
    return output_category(category)


# outputs
def output_category(category):
    return {
        'id': category['_id'],
        'slug': category['slug'],
        'label': category['label'],
        'title': category['title'],
        'caption': category['caption'],
        'cat_ids': category['cat_ids'],
        'src': category['src'],
    }
