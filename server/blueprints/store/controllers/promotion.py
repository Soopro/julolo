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

    promo = current_app.mongodb.Promotion.find_one_by_slug(promo_slug)
    if not promo:
        raise StorePromoNotFound

    if not promo['favorite_id']:
        return []

    # use default store for now
    store = current_app.mongodb.Store.find_one_default()
    taoke = connect_taoke(store)
    try:
        items = taoke.list_favorite_items(favorite_id=promo['favorite_id'],
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
        'is_collection': True,
        'url': url,
    }
