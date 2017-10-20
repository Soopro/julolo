# coding=utf-8
from __future__ import absolute_import

from flask import current_app

from utils.response import output_json
from utils.request import get_args, get_param
from utils.misc import parse_int

from ..errors import StoreGoodsError


@output_json
def list_events():
    events = [
        {
            '_id': 213,
            'src': 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg',
            'title': 'Testgy',
            'slug': 'test',
            'caption': u'',
            'type': None,
        },
        {
            '_id': 213,
            'src': 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg',
            'title': 'Testgy',
            'slug': 'test',
            'caption': u'',
            'type': None,
        },
        {
            '_id': 213,
            'src': 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg',
            'title': 'Testgy',
            'slug': 'test',
            'caption': u'',
            'type': None,
        },
    ]

    return [output_event(event) for event in events]


@output_json
def get_event(evt_slug):
    event = {
        '_id': 213,
        'src': 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg',
        'title': 'Event',
        'slug': 'test',
        'cat_ids': None,
        'caption': u'Event, in the event of, in any event, in the event, main event, sports event, in the event that, current event, event management, event manager, sporting event',
        'type': None,
    }
    return output_event(event)


@output_json
def list_event_items(evt_slug):
    paged = parse_int(get_args('paged'), 1, 1)
    perpage = parse_int(get_args('perpage'), 60, 1)

    favorite_id = '12968308'
    try:
        event_items = current_app.taoke.\
            list_favorite_items(favorite_id=favorite_id,
                                paged=paged,
                                perpage=perpage)
    except Exception as e:
        raise StoreGoodsError(e)

    return [output_event_item(item) for item in event_items]


# outputs
def output_event(event):
    return {
        'id': event['_id'],
        'src': event['src'],
        'slug': event['slug'],
        'title': event['title'],
        'caption': event['caption'],
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
