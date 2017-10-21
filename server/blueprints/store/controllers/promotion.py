# coding=utf-8
from __future__ import absolute_import

from flask import current_app

from utils.response import output_json
from utils.request import get_args
from utils.misc import parse_int

from helpers.media import media_safe_src
from helpers.user import connect_taoke

from ..errors import StorePromoNotFound, StorePromoItemsError


@output_json
def list_promotions():
    promotions = current_app.mongodb.Promotion.find_activated()
    return [output_promo(promo) for promo in promotions]


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

    fav_id = promo['favorite_id']

    taoke = connect_taoke()
    try:
        promo_items = taoke.list_favorite_items(favorite_id=fav_id,
                                                paged=paged,
                                                perpage=perpage)
    except Exception as e:
        raise StorePromoItemsError(e)

    return [output_promo_item(item) for item in promo_items]


# outputs
def output_promo(promo):
    return {
        'id': promo['_id'],
        'src': promo['src'],
        'slug': promo['slug'],
        'title': promo['title'],
        'poster': media_safe_src(promo['poster']),
        'caption': promo['caption'],
        'updated': promo['updated'],
        'creation': promo['creation']
    }


def output_promo_item(item):
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
