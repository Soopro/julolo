# coding=utf-8
from __future__ import absolute_import

from flask import current_app, g

from utils.response import output_json
from utils.request import get_args
from utils.model import make_offset_paginator
from utils.misc import parse_int

from helpers.media import media_safe_src
from helpers.user import connect_taoke

from ..errors import StoreEventNotFound, StoreEventItemsError


@output_json
def list_events():
    store = g.store
    event_limit = store['event_limit'] or 6
    events = current_app.mongodb.Event.find_activated()
    make_offset_paginator(events, 0, event_limit)
    return [output_event(event) for event in events]


@output_json
def get_event(evt_slug):
    event = current_app.mongodb.Event.find_one_by_slug(evt_slug)
    if not event:
        raise StoreEventNotFound
    return output_event(event)


@output_json
def list_event_items(evt_slug):
    paged = parse_int(get_args('paged'), 1, 1)
    perpage = parse_int(get_args('perpage'), 60, 1)

    event = current_app.mongodb.Event.find_one_by_slug(evt_slug)
    if not event:
        raise StoreEventNotFound(evt_slug)

    fav_id = event['favorite_id']

    taoke = connect_taoke()
    try:
        event_items = taoke.list_favorite_items(favorite_id=fav_id,
                                                paged=paged,
                                                perpage=perpage)
    except Exception as e:
        raise StoreEventItemsError(e)

    return [output_event_item(item) for item in event_items]


# outputs
def output_event(event):
    return {
        'id': event['_id'],
        'slug': event['slug'],
        'title': event['title'],
        'poster': media_safe_src(event['poster']),
        'caption': event['caption'],
        'updated': event['updated'],
        'creation': event['creation'],
    }


def output_event_item(item):
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
