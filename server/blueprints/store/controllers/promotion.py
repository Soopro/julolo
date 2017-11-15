# coding=utf-8
from __future__ import absolute_import

from flask import current_app, g

from utils.response import output_json
from utils.request import get_args
from utils.model import make_paginator, attach_extend
from utils.misc import parse_int

from helpers.media import media_safe_src, media_safe_splash
from helpers.common import connect_taoke, convert_date, convert_parice

from ..errors import StorePromoNotFound, StorePromoItemsError


@output_json
def list_promotions():
    paged = parse_int(get_args('paged'), 1, 1)
    perpage = parse_int(get_args('perpage'), 60, 1)

    promotions = current_app.mongodb.Promotion.find_activated()
    p = make_paginator(promotions, paged, perpage)
    return attach_extend(
        [output_promo(promo) for promo in promotions],
        {'_more': p.has_next, '_count': p.count}
    )


@output_json
def get_promotion(promo_slug):
    promo = current_app.mongodb.Promotion.find_one_by_slug(promo_slug)
    if not promo:
        raise StorePromoNotFound
    return output_promo(promo)


@output_json
def list_promotion_items(promo_slug):
    paged = parse_int(get_args('paged'), 1, 1)
    perpage = parse_int(get_args('perpage'), 60, 1)
    timestamp = parse_int(get_args('timestamp'))

    promo = current_app.mongodb.Promotion.find_one_by_slug(promo_slug)
    if not promo:
        raise StorePromoNotFound

    if promo['favorite_key']:
        results = _list_commodity_favorites(promo['favorite_key'],
                                            paged,
                                            perpage,
                                            timestamp)
    elif promo['favorite_id']:
        results = _list_taoke_favorites(promo['favorite_id'],
                                        paged,
                                        perpage)
    else:
        results = []

    return results


# helpers
def _list_commodity_favorites(favorite_key, paged, perpage, timestamp):
    high_commission = g.store['high_commission']
    items = current_app.mongodb.\
        Commodity.find_favorites(favorite_key, timestamp, high_commission)
    p = make_paginator(items, paged, perpage)
    return attach_extend(
        [output_promo_commodity(item) for item in items],
        {'_more': p.has_next}
    )


def _list_taoke_favorites(favorite_id, paged, perpage):
    store = current_app.mongodb.Store.find_one_default()
    taoke = connect_taoke(store)
    try:
        items = taoke.list_favorite_items(favorite_id=favorite_id,
                                          paged=paged,
                                          perpage=perpage)
    except Exception as e:
        raise StorePromoItemsError(e)

    results_count = len(items)

    return attach_extend(
        [output_promo_item(item) for item in items],
        {'_more': results_count >= perpage}
    )


# outputs
def output_promo(promo):
    return {
        'id': promo['_id'],
        'slug': promo['slug'],
        'title': promo['title'],
        'poster': media_safe_src(promo['poster'], promo['updated']),
        'splash': media_safe_splash(promo['splash'], promo['updated']),
        'caption': promo['caption'],
        'updated': promo['updated'],
        'creation': promo['creation']
    }


def output_promo_commodity(item):
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


def output_promo_item(item):
    price = item.get('zk_final_price_wap') or item.get('zk_final_price')
    url = item.get('coupon_click_url') or item.get('click_url') or False
    return {
        'id': item['num_iid'],
        'item_id': item['num_iid'],
        'shop_title': item['shop_title'],
        'type': item['user_type'],
        'price': price,
        'title': item['title'],
        'volume': item['volume'],
        'src': item['pict_url'],
        'figures': item.get('small_images', {}).get('string', []),
        'category': item.get('category'),
        'coupon_info': item.get('coupon_info'),
        'start_time': item.get('coupon_start_time'),
        'end_time': item.get('coupon_end_time'),
        'url': url,
    }
