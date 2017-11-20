# coding=utf-8
from __future__ import absolute_import

from flask import current_app

from utils.response import output_json
from utils.request import get_args
from utils.model import make_paginator, attach_extend
from utils.misc import parse_int

from helpers.media import media_safe_src, media_safe_splash
from helpers.common import convert_date, convert_parice

from ..errors import StoreEventNotFound


@output_json
def list_events():
    paged = parse_int(get_args('paged'), 1, 1)
    perpage = parse_int(get_args('perpage'), 60, 1)

    events = current_app.mongodb.Event.find_activated()
    p = make_paginator(events, paged, perpage)
    return attach_extend(
        [output_event(event) for event in events],
        {'_more': p.has_next, '_count': p.count}
    )


@output_json
def get_event(event_slug):
    event = current_app.mongodb.Event.find_one_by_slug(event_slug)
    if not event:
        raise StoreEventNotFound
    return output_event(event)


@output_json
def list_event_items(event_slug):
    paged = parse_int(get_args('paged'), 1, 1)
    perpage = parse_int(get_args('perpage'), 60, 1)
    timestamp = parse_int(get_args('timestamp'))

    items = current_app.mongodb.Commodity.find_by_event(event_slug, timestamp)
    p = make_paginator(items, paged, perpage)
    return attach_extend(
        [output_event_commodity(item) for item in items],
        {'_more': p.has_next, '_count': p.count}
    )


# outputs
def output_event(event):
    return {
        'id': event['_id'],
        'slug': event['slug'],
        'title': event['title'],
        'poster': media_safe_src(event['poster'], event['updated']),
        'splash': media_safe_splash(event['splash'], event['updated']),
        'caption': event['caption'],
        'updated': event['updated'],
        'creation': event['creation']
    }


def output_event_commodity(item):
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
