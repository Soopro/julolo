# coding=utf-8
from __future__ import absolute_import

from flask import current_app

from utils.response import output_json
from utils.request import get_args, get_param
from utils.misc import parse_int

from apiresps.validations import Struct

from ..errors import StoreCouponError


@output_json
def list_coupons():
    paged = parse_int(get_args('paged'), 1, 1)
    perpage = parse_int(get_args('perpage'), 60, 1)

    try:
        coupons = current_app.taoke.list_coupons(paged=paged,
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

    try:
        coupons = current_app.taoke.list_coupons(search_key=keyword,
                                                 categories=categories,
                                                 paged=paged,
                                                 perpage=perpage)
    except Exception as e:
        raise StoreCouponError(e)

    return [output_coupon(coupon) for coupon in coupons]


# outputs
def output_coupon(coupon):
    return {
        'id': coupon['num_iid'],
        'shop': coupon['shop_title'],
        'type': coupon['user_type'],
        'price': coupon['zk_final_price'],
        'title': coupon['title'],
        'volume': coupon['volume'],
        'src': coupon['pict_url'],
        'figures': coupon['small_images'].get('string', []),
        'coupon': coupon['coupon_info'],
        'category': coupon['category'],
        'start_time': coupon['coupon_start_time'],
        'end_time': coupon['coupon_end_time'],
        'description': coupon['item_description'],
        'coupon_url': coupon['coupon_click_url']
    }
