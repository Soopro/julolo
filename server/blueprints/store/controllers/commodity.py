# coding=utf-8
from __future__ import absolute_import

from flask import current_app

from utils.response import output_json
from utils.request import get_args, get_param
from utils.model import make_paginator, attach_extend
from utils.misc import parse_int, format_date

from apiresps.validations import Struct

from ..errors import StoreCategoryInvalid


@output_json
def list_commodities():
    paged = parse_int(get_args('paged'), 1, 1)
    perpage = parse_int(get_args('perpage'), 12, 1)
    timestamp = parse_int(get_args('timestamp'))
    categories = get_args('categories')

    cids = _convert_categories(categories)

    items = current_app.mongodb.Commodity.find_live(cids, timestamp)
    p = make_paginator(items, paged, perpage)

    return attach_extend(
        [output_commodity(item) for item in items],
        {'_more': p.has_next, '_count': p.count}
    )


@output_json
def search_commodities():
    paged = get_param('paged', Struct.Int, default=1)
    perpage = get_param('perpage', Struct.Int, default=60)
    keyword = get_param('keyword', Struct.Attr, default=u'')
    timestamp = parse_int(get_args('timestamp'))
    categories = get_args('categories')

    cids = _convert_categories(categories)

    paged = parse_int(paged, 1, 1)
    perpage = parse_int(perpage, 1, 1)

    if not keyword:
        return []

    items = current_app.mongodb.Commodity.search(keyword, cids, timestamp)
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
            cids = [cate.strip() for cate in categories.split(',')]
        elif isinstance(categories, list):
            cids = [cate.strip() for cate in categories
                    if isinstance(cate, basestring)]
    except Exception as e:
        raise StoreCategoryInvalid(e)

    return cids


def _convert_parice(price):
    try:
        return u'{:,.2f}'.format(price / 100.0)
    except Exception:
        return None


def _convert_date(date):
    return format_date(date, '%Y-%m-%d')


# outputs
def output_commodity(item):
    return {
        'id': item['_id'],
        'shop_name': item['shop_name'],
        'type': item['shop_type'],
        'title': item['title'],
        'volume': item['volume'],
        'src': item['src'],
        'price': _convert_parice(item['price']),
        'category': item['category'],
        'coupon_info': item['coupon_info'],
        'start_time': _convert_date(item['start_time']),
        'end_time': _convert_date(item['end_time']),
        'url': item['coupon_click_url'] or item['click_url']
    }
