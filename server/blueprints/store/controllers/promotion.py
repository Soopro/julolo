# coding=utf-8
from __future__ import absolute_import

from flask import current_app

from utils.response import output_json
from utils.request import get_args, get_param
from utils.misc import parse_int

from apiresps.validations import Struct


@output_json
def list_promotions():
    promotions = [
        {
            '_id': 213,
            'src': 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg',
            'label': 'Testgy',
            'caption': u'',
        },
        {
            '_id': 213,
            'src': 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg',
            'label': 'Testgy',
            'caption': u'',
        },
        {
            '_id': 213,
            'src': 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg',
            'label': 'Testgy',
            'caption': u'',
        },
        {
            '_id': 213,
            'src': 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg',
            'label': 'Testgy',
            'caption': u'',
        },
        {
            '_id': 213,
            'src': 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg',
            'label': 'Testgy',
            'caption': u'',
        },
    ]

    return [output_promo(promo) for promo in promotions]


@output_json
def list_banners():
    banner = {
        '_id': '123',
        'label': '123',
        'caption': u'',
        'slot': 'index',
        'src': 'http://www.3dmgame.com/uploads/allimg/150608/276_150608083901_1.jpg'
    }
    banners = [banner, banner]
    return [output_banner(banner) for banner in banners]


@output_json
def get_banner(slot):
    banner = {
        '_id': '123',
        'label': '123',
        'caption': u'',
        'slot': 'index',
        'src': 'http://www.3dmgame.com/uploads/allimg/150608/276_150608083901_1.jpg'
    }
    return output_banner(banner)


# outputs
def output_promo(promo):
    return {
        'id': promo['_id'],
        'src': promo['src'],
        'label': promo['label'],
        'caption': promo['caption'],
    }


def output_banner(banner):
    return {
        'id': banner['_id'],
        'label': banner['label'],
        'caption': banner['caption'],
        'slot': banner['slot'],
        'src': banner['src']
    }
