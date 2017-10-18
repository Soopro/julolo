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
            'src': 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg',
            'label': 'Testgy',
            'caption': u'',
        },
        {
            'src': 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg',
            'label': 'Testgy',
            'caption': u'',
        },
        {
            'src': 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg',
            'label': 'Testgy',
            'caption': u'',
        },
        {
            'src': 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg',
            'label': 'Testgy',
            'caption': u'',
        },
        {
            'src': 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg',
            'label': 'Testgy',
            'caption': u'',
        },
    ]

    return [output_promo(promo) for promo in promotions]


@output_json
def get_advertising(ad_slot):
    ad = {
        '_id': '123',
        'label': '123',
        'caption': u'',
        'slot': 'index',
        'src': 'http://www.3dmgame.com/uploads/allimg/150608/276_150608083901_1.jpg'
    }
    return output_ad(ad)


# outputs
def output_promo(promo):
    return {
        'id': promo['_id'],
        'src': promo['src'],
        'label': promo['label'],
        'caption': promo['caption'],
    }


def output_ad(ad):
    return {
        'id': ad['_id'],
        'label': ad['label'],
        'caption': ad['caption'],
        'slot': ad['slot'],
        'src': ad['src']
    }
