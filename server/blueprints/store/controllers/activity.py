# coding=utf-8
from __future__ import absolute_import

from flask import current_app

from utils.response import output_json
from utils.request import get_args
from utils.model import make_paginator, attach_extend
from utils.misc import parse_int

from helpers.media import media_safe_src, media_safe_splash
from helpers.common import convert_date, convert_parice

from ..errors import StoreActivityNotFound


@output_json
def list_activities():
    paged = parse_int(get_args('paged'), 1, 1)
    perpage = parse_int(get_args('perpage'), 60, 1)

    activitys = current_app.mongodb.Activity.find_activated()
    p = make_paginator(activitys, paged, perpage)
    return attach_extend(
        [output_activity(activity) for activity in activitys],
        {'_more': p.has_next, '_count': p.count}
    )


@output_json
def get_activity(activity_slug):
    activity = current_app.mongodb.Activity.find_one_by_slug(activity_slug)
    if not activity:
        raise StoreActivityNotFound
    return output_activity(activity)


@output_json
def list_activity_items(activity_slug):
    paged = parse_int(get_args('paged'), 1, 1)
    perpage = parse_int(get_args('perpage'), 60, 1)
    timestamp = parse_int(get_args('timestamp'))

    items = current_app.mongodb.\
        Commodity.find_by_activity(activity_slug, timestamp)
    p = make_paginator(items, paged, perpage)
    return attach_extend(
        [output_activity_commodity(item) for item in items],
        {'_more': p.has_next, '_count': p.count}
    )


# outputs
def output_activity(activity):
    return {
        'id': activity['_id'],
        'slug': activity['slug'],
        'title': activity['title'],
        'poster': media_safe_src(activity['poster'], activity['updated']),
        'splash': media_safe_splash(activity['splash'], activity['updated']),
        'caption': activity['caption'],
        'updated': activity['updated'],
        'creation': activity['creation']
    }


def output_activity_commodity(item):
    return {
        'id': item['_id'],
        'shop_title': item['shop_title'],
        'type': item['shop_type'],
        'title': item['title'],
        'volume': item['volume'] or u'(^_^)',
        'src': item['src'],
        'price': convert_parice(item['price']),
        'category': item['category'],
        'coupon_id': item['coupon_id'],
        'coupon_info': item['coupon_info'],
        'start_time': convert_date(item['start_time']),
        'end_time': convert_date(item['end_time']),
        'url': item['coupon_click_url'] or item['click_url'],
    }
