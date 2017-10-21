# coding=utf-8
from __future__ import absolute_import

from flask import g

from utils.response import output_json
from utils.request import get_args, get_param
from utils.misc import parse_int

from helpers.user import connect_taoke

from apiresps.validations import Struct

from ..errors import StoreCouponError, StoreCouponGenerateFailed


@output_json
def list_coupons():
    paged = parse_int(get_args('paged'), 1, 1)
    perpage = parse_int(get_args('perpage'), 60, 1)
    categories = get_args('categories')

    taoke = connect_taoke()

    try:
        coupons = taoke.list_coupons(categories=categories,
                                     paged=paged,
                                     perpage=perpage)
    except Exception as e:
        raise StoreCouponError(e)

    return [output_coupon(coupon) for coupon in coupons]


@output_json
def search_coupons():
    paged = get_param('paged', Struct.Int, default=1)
    perpage = get_param('perpage', Struct.Int, default=60)
    keyword = get_param('keyword', Struct.Attr, default=u'')
    categories = get_param('categories', Struct.List, default=[])

    paged = parse_int(paged, 1, 1)
    perpage = parse_int(perpage, 1, 1)

    if not keyword:
        return []

    taoke = connect_taoke()

    try:
        coupons = taoke.list_coupons(search_key=keyword,
                                     categories=categories,
                                     paged=paged,
                                     perpage=perpage)
    except Exception as e:
        raise StoreCouponError(e)

    return [output_coupon(coupon) for coupon in coupons]


@output_json
def generate_coupon_code():
    text = get_param('text', Struct.Attr, True)
    url = get_param('url', Struct.Url, True)
    logo = get_param('logo', Struct.Url)

    store = g.store

    if not store['allow_tpwd']:
        return {
            'code': False,
        }

    taoke = connect_taoke()

    try:
        code = taoke.create_code(text=text, url=url, logo=logo)
    except Exception as e:
        raise StoreCouponGenerateFailed(e)
    return {
        'code': code
    }


# outputs
def output_coupon(coupon):
    return {
        'id': coupon['num_iid'],
        'shop': coupon['shop_title'],
        'type': coupon['user_type'],
        'title': coupon['title'],
        'volume': coupon['volume'],
        'src': coupon['pict_url'],
        'figures': coupon.get('small_images', {}).get('string', []),
        'price': coupon.get('zk_final_price'),
        'coupon': coupon.get('coupon_info'),
        'category': coupon.get('category'),
        'start_time': coupon.get('coupon_start_time'),
        'end_time': coupon.get('coupon_end_time'),
        'description': coupon.get('item_description'),
        'url': coupon.get('coupon_click_url')
    }
