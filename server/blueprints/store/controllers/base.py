# coding=utf-8
from __future__ import absolute_import

from flask import g

from utils.response import output_json
from utils.request import get_args
from utils.misc import parse_int

from helpers.user import connect_taoke

from ..errors import StoreCouponError


@output_json
def get_store():
    store = g.store
    return {
        'id': store['_id'],
        'event_limit': store['event_limit'],
        'promotion_limit': store['promotion_limit'],
        'allow_tpwd': store['allow_tpwd'],
        'tpwd_msg': store['tpwd_msg'],
        'cat_ids': store['cat_ids'],
        'updated': store['updated'],
        'creation': store['creation']
    }


@output_json
def list_newest():
    paged = parse_int(get_args('paged'), 1, 1)
    perpage = parse_int(get_args('perpage'), 60, 1)

    store = g.store
    categories = store['cat_ids'] or None

    taoke = connect_taoke()

    try:
        coupons = taoke.list_coupons(categories=categories,
                                     paged=paged,
                                     perpage=perpage)
    except Exception as e:
        raise StoreCouponError(e)

    return [output_newest(coupon) for coupon in coupons]


# outputs
def output_newest(coupon):
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
