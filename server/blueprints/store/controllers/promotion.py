# coding=utf-8
from __future__ import absolute_import

from flask import current_app

from utils.response import output_json
from utils.request import get_args, get_param
from utils.misc import parse_int

from ..errors import StoreGoodsError


@output_json
def list_promotions():
    promo_type = get_args('type')

    promotions = [
        {
            '_id': 213,
            'src': 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg',
            'title': 'Testgy',
            'slug': 'test',
            'caption': u'',
            'cat_ids': None,
            'keyword': '连裤袜',
            'type': None,
        },
        {
            '_id': 213,
            'src': 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg',
            'title': 'Testgy',
            'slug': 'test',
            'cat_ids': None,
            'caption': u'',
            'keyword': '连裤袜',
            'type': None,
        },
        {
            '_id': 213,
            'src': 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg',
            'title': 'Testgy',
            'slug': 'test',
            'cat_ids': None,
            'caption': u'',
            'keyword': '连裤袜',
            'type': None,
        },
        {
            '_id': 213,
            'src': 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg',
            'title': 'Testgy',
            'slug': 'test',
            'cat_ids': None,
            'caption': u'',
            'keyword': '连裤袜',
            'type': None,
        },
        {
            '_id': 213,
            'src': 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg',
            'title': 'Testgy',
            'cat_ids': '14',
            'slug': 'test',
            'caption': u'',
            'keyword': '连裤袜',
            'type': None,
        },
        {
            '_id': '123',
            'title': '123',
            'cat_ids': '29, 98',
            'caption': u'',
            'slug': 'test',
            'type': 'banner',
            'keyword': '连裤袜',
            'src': 'http://www.3dmgame.com/uploads/allimg/150608/276_150608083901_1.jpg'
        },
        {
            '_id': '123',
            'title': '123',
            'caption': u'',
            'slug': 'test',
            'cat_ids': '16',
            'type': 'banner',
            'keyword': '连裤袜',
            'src': 'http://www.3dmgame.com/uploads/allimg/150608/276_150608083901_1.jpg'
        }
    ]

    if promo_type == 'banner':
        promotions = [promo for promo in promotions
                      if promo['type'] == 'banner']
    return [output_promo(promo) for promo in promotions]


@output_json
def get_promotion(promo_slug):
    promo = {
        '_id': '123',
        'slug': 'test',
        'type': 'banner',
        'title': '哟哟啊啥的',
        'cat_ids': '29, 98',
        'caption': u'',
        'src': 'http://www.3dmgame.com/uploads/allimg/150608/276_150608083901_1.jpg',
        'keyword': '',
    }
    return output_promo(promo)


@output_json
def list_promotion_items(promo_slug):
    paged = parse_int(get_args('paged'), 1, 1)
    perpage = parse_int(get_args('perpage'), 60, 1)

    favorite_id = '12968308'
    try:
        promo_items = current_app.taoke.\
            list_favorite_items(favorite_id=favorite_id,
                                paged=paged,
                                perpage=perpage)
    except Exception as e:
        raise StoreGoodsError(e)

    return [output_promo_item(promo_item) for promo_item in promo_items]


# outputs
def output_promo(promo):
    return {
        'id': promo['_id'],
        'src': promo['src'],
        'slug': promo['slug'],
        'cat_ids': promo['cat_ids'],
        'title': promo['title'],
        'caption': promo['caption'],
        'type': promo['type'],
        'keyword': promo['keyword'],
    }


def output_promo_item(item):
    price = item.get('zk_final_price_wap') or item.get('zk_final_price')
    url = item.get('coupon_click_url') or item.get('click_url')
    return {
        'id': item['num_iid'],
        'shop': item['shop_title'],
        'type': item['user_type'],
        'price': price,
        'title': item['title'],
        'volume': item['volume'],
        'src': item['pict_url'],
        'category': item.get('category'),
        'figures': item.get('small_images', {}).get('string', []),
        'coupon': item.get('coupon_info'),
        'start_time': item.get('coupon_start_time'),
        'end_time': item.get('coupon_end_time'),
        'url': url,
    }
