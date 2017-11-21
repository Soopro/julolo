# coding=utf-8
from __future__ import absolute_import

from flask import current_app, g
import re

from utils.response import output_json
from utils.request import get_args, get_param
from utils.misc import parse_int

from helpers.common import connect_taoke

from apiresps.validations import Struct

from ..errors import StoreCouponError, StoreCouponGenerateFailed


@output_json
def list_item_coupons():
    paged = parse_int(get_args('paged'), 1, 1)
    perpage = parse_int(get_args('perpage'), 60, 1)
    categories = get_args('categories')

    if categories:
        perpage = _safe_perpage(paged, perpage)
    else:
        perpage = _safe_perpage(paged, perpage, limit=10000)

    if perpage <= 0:
        return []

    taoke = connect_taoke()

    try:
        coupons = taoke.list_coupons(categories=categories,
                                     paged=paged,
                                     perpage=perpage)
    except Exception as e:
        current_app.logger.error(StoreCouponError(e))
        coupons = []

    return [output_coupon(coupon) for coupon in coupons]


@output_json
def search_item_coupons():
    paged = get_param('paged', Struct.Int, default=1)
    perpage = get_param('perpage', Struct.Int, default=60)
    keyword = get_param('keyword', Struct.Attr, default=u'')
    categories = get_param('categories')

    paged = parse_int(paged, 1, 1)
    perpage = parse_int(perpage, 1, 1)

    if not keyword:
        return []

    perpage = _safe_perpage(paged, perpage)
    if perpage <= 0:
        return []

    taoke = connect_taoke()

    try:
        coupons = taoke.list_coupons(search_key=keyword,
                                     categories=categories,
                                     paged=paged,
                                     perpage=perpage)
    except Exception as e:
        current_app.logger.error(StoreCouponError(e))
        coupons = []

    return [output_coupon(coupon) for coupon in coupons]


@output_json
def generate_coupon_code():
    text = get_param('text', Struct.Attr, True)
    url = get_param('url', Struct.Url, True)
    logo = get_param('logo', Struct.Url)
    item = get_param('item', Struct.Dict)

    store = g.store

    if not store['allow_tpwd']:
        return {
            'code': False,
            'msg': store['tpwd_msg'],
        }

    taoke = connect_taoke()
    converted_url = _convert_url_pid(taoke, store['pid'], url, item)
    to_url = converted_url or url

    try:
        code = taoke.create_code(text=text, url=to_url, logo=logo)
    except Exception as e:
        raise StoreCouponGenerateFailed(e)

    current_app.sa_mod.record_customer()

    if current_app.debug:
        print 'url:', url
        print 'converted_url:', converted_url
        print item.get('id')

    if converted_url:
        msg = store['tpwd_msg']
    else:
        msg = u'{}~'.format(store['tpwd_msg'])

    return {
        'code': code,
        'msg': msg,
        'converted': bool(converted_url),
    }


# helpers
def _safe_perpage(paged, perpage, limit=100):
    # limit total results under 100,
    # otherwise taobao might return duplicated results.
    # sometime results could be more 100, seems is distributed cache.
    _query_total = paged * perpage
    if _query_total >= limit:
        perpage = perpage - (_query_total - limit)
    return perpage


def _convert_url_pid(taoke, pid, url, item):
    try:
        _url_pid = taoke.PID_PATTERN.search(url).group(1)
    except Exception:
        _url_pid = None

    if _url_pid == pid:
        return url

    item_id = item.get('item_id')
    activity_id = item.get('coupon_id')

    converted_url = taoke.convert_url(url, item_id, activity_id, pid)

    # incase api is overrun
    # if not converted_url:
    #     item_id = item.get('item_id')
    #     item_title = item.get('title')
    #     item_shop_title = item.get('shop_title')

    #     if item_title and item_id and item_shop_title:
    #         try:
    #             results = taoke.list_coupons(search_key=item_title,
    #                                          perpage=60)
    #         except Exception:
    #             return None
    #         results = [_item for _item in results
    #                    if _item.get('shop_title') == item_shop_title and
    #                    str(_item.get('num_iid')) == item_id]
    #         if results:
    #             converted_url = results[0].get('coupon_click_url')

    return converted_url


# outputs
def output_coupon(coupon):
    return {
        'id': coupon['num_iid'],
        'item_id': coupon['num_iid'],
        'shop_title': coupon['shop_title'],
        'seller_id': coupon['seller_id'],
        'type': coupon['user_type'],
        'title': coupon['title'],
        'volume': coupon['volume'],
        'src': coupon['pict_url'],
        'figures': coupon.get('small_images', {}).get('string', []),
        'price': coupon.get('zk_final_price'),
        'coupon_info': coupon.get('coupon_info'),
        'category': coupon.get('category'),
        'start_time': coupon.get('coupon_start_time'),
        'end_time': coupon.get('coupon_end_time'),
        'description': coupon.get('item_description'),
        'url': coupon.get('coupon_click_url'),
        'is_extra': True,
    }
