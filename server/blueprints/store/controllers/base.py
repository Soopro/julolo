# coding=utf-8
from __future__ import absolute_import

from flask import g, current_app

from utils.response import output_json
from utils.request import get_args
from utils.model import make_paginator, attach_extend
from utils.misc import parse_int

from ..errors import StoreCouponError


@output_json
def get_store():
    store = g.store
    return {
        'id': store['_id'],
        'event_limit': store['event_limit'],
        'promotion_limit': store['promotion_limit'],
        'tpwd': store['tpwd'],
        'updated': store['updated'],
        'creation': store['creation']
    }


@output_json
def list_newest():
    paged = parse_int(get_args('paged'), 1, 1)
    perpage = parse_int(get_args('perpage'), 12, 1)

    items = current_app.mongodb.Commodity.find_all()
    p = make_paginator(items, paged, perpage)
    return attach_extend(
        [output_newest(item) for item in items],
        {'_more': p.has_more, '_count': p.count}
    )


# helpers
def _safe_perpage(paged, perpage, limit=100):
    # limit total results under 100,
    # otherwise taobao might return duplicated results.
    # sometime results could be more 100, seems is distributed cache.
    _query_total = paged * perpage
    if _query_total >= limit:
        perpage = perpage - (_query_total - limit)
    return perpage


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
