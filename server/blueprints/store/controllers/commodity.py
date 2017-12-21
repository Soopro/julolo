# coding=utf-8
from __future__ import absolute_import

from flask import current_app, g

from utils.response import output_json
from utils.request import get_args, get_param
from utils.model import make_paginator, attach_extend
from utils.misc import parse_int

from helpers.common import convert_date, convert_price
from apiresps.validations import Struct

from ..errors import StoreCategoryInvalid, StoreCommodityNotFound


@output_json
def list_commodities():
    paged = parse_int(get_args('paged'), 1, 1)
    perpage = parse_int(get_args('perpage'), 12, 1)
    timestamp = parse_int(get_args('timestamp'))
    categories = get_args('categories')
    is_newest = get_args('newest')

    store = g.store
    if is_newest and not categories:
        categories = store['cat_ids']

    cids = _convert_categories(categories)

    items = current_app.mongodb.\
        Commodity.find_live(cids, timestamp, store['sort_type'])
    p = make_paginator(items, paged, perpage)

    return attach_extend(
        [output_commodity(item) for item in items],
        {'_more': p.has_next, '_count': p.count}
    )


@output_json
def get_commodity(co_id):
    item = current_app.mongodb.Commodity.find_one_by_id(co_id)
    if not item:
        raise StoreCommodityNotFound

    return output_commodity(item)


@output_json
def search_commodities():
    paged = get_param('paged', Struct.Int, default=1)
    perpage = get_param('perpage', Struct.Int, default=60)
    keywords = get_param('keywords', Struct.List, default=[])
    timestamp = parse_int(get_args('timestamp'))
    categories = get_args('categories')

    store = g.store

    cids = _convert_categories(categories)

    paged = parse_int(paged, 1, 1)
    perpage = parse_int(perpage, 1, 1)

    if not keywords:
        return []
    items = current_app.mongodb.\
        Commodity.search(keywords, cids, timestamp, store['sort_type'])
    p = make_paginator(items, paged, perpage)

    return attach_extend(
        [output_commodity(item) for item in items],
        {'_more': p.has_next, '_count': p.count}
    )


# helpers
def _convert_categories(categories):
    if not categories:
        return None
    try:
        if isinstance(categories, basestring):
            cids = [cate for cate in categories.split(',')]
        elif isinstance(categories, list):
            cids = [unicode(cid) for cid in categories
                    if isinstance(cid, (int, unicode))]
    except Exception as e:
        raise StoreCategoryInvalid(e)

    return cids


# outputs
def output_commodity(item):
    return {
        'id': item['_id'],
        'item_id': item['item_id'],
        'shop_title': item['shop_title'],
        'type': item['shop_type'],
        'title': item['title'],
        'volume': item['volume'] or u'(^_^)',
        'src': item['src'],
        'price': convert_price(item['price']),
        'category': item['category'],
        'coupon_id': item['coupon_id'],
        'coupon_info': item['coupon_info'],
        'start_time': convert_date(item['start_time']),
        'end_time': convert_date(item['end_time']),
        'url': item['coupon_click_url'] or item['click_url'],
    }
