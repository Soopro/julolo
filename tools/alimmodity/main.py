# coding=utf-8
from __future__ import absolute_import

import os
import json

from .csv import load_csv
from .xls import load_xls


COUPON_CLICK_BASE_URL = 'https://uland.taobao.com/coupon/'
CLICK_BASE_URL = 'https://s.click.taobao.com/'


def _load_policy(policy_path):
    _policy = {
        'size': 500,
        'category': {},
    }
    if os.path.isfile(policy_path):
        try:
            with open(policy_path) as f:
                policy = json.load(f)
            if not isinstance(policy, dict):
                raise Exception('must be a dict.')
        except Exception as e:
            raise Exception('Invalid policy file: {}'.format(e))
        _policy.update(policy)

    return _policy


def _shop_type(input_type):
    if isinstance(input_type, str):
        input_type = input_type.decode('utf-8')
    if input_type == u'天猫':
        return 1
    else:
        return 0


def _parse_int(input):
    try:
        return int(input)
    except Exception:
        return 0


def _process_links(item):
    click_link = item.get(u'淘宝客链接', u'')
    coupon_click_link = item.get(u'商品优惠券推广链接', u'')
    _link = item.get(u'推广链接', u'')
    if _link.startswith(COUPON_CLICK_BASE_URL):
        coupon_click_link = _link
    elif _link.startswith(CLICK_BASE_URL):
        click_link = _link
    return coupon_click_link, click_link


def _chunks(input_list, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(input_list), n):
        yield input_list[i:i + n]


def convert(file_path, output_dir=None, policy_path=None):
    fname, ext = os.path.splitext(file_path)
    if not os.path.isfile(file_path):
        raise Exception('Invalid file, file path is not exists.')
    if ext == '.csv':
        sheetdata = load_csv(file_path)
    elif ext == '.xls':
        sheetdata = load_xls(file_path)
    else:
        raise Exception('Invalid file, must be .csv or .xls')

    if not output_dir:
        output_dir = fname
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    policy = _load_policy(policy_path)

    split_size = min(max(_parse_int(policy['size']), 100), 10000)

    loop = 1
    for farg_data in _chunks(sheetdata, split_size):
        output_farg = []
        for item in farg_data:
            try:
                item_id = int(item.get(u'商品id'))
            except Exception:
                item_id = None

            if not item_id:
                raise Exception('item id is missing.')

            category = item.get(u'商品一级类目', u'')
            cid = policy['category'].get(category)
            if not cid:
                continue

            coupon_click_link, click_link = _process_links(item)

            try:
                output_farg.append({
                    'item_id': item_id,
                    'title': item.get(u'商品名称', u''),
                    'pic_url': item.get(u'商品主图', u''),
                    'detail_url': item.get(u'商品详情页链接地址', u''),
                    'category': category,
                    'cid': cid,
                    'price': float(item.get(u'商品价格', 0)),
                    'volume': int(item.get(u'商品月销量', 0)),
                    'income_rate': float(item.get(u'收入比率', 0)),
                    'commission': float(item.get(u'佣金', 0)),
                    'seller_im': item.get(u'卖家旺旺', u''),
                    'seller_id': item.get(u'卖家id', u''),
                    'shop_title': item.get(u'店铺名称', u''),
                    'shop_type': _shop_type(item.get(u'平台类型', u'')),
                    'coupon_id': item.get(u'优惠券id', u''),
                    'coupon_volume': int(item.get(u'优惠券总量'), 0),
                    'coupon_remine': int(item.get(u'优惠券剩余量', 0)),
                    'coupon_info': item.get(u'优惠券面额', u''),
                    'coupon_start_time': item.get(u'优惠券开始时间', u''),
                    'coupon_end_time': item.get(u'优惠券结束时间', u''),
                    'coupon_url': item.get(u'优惠券链接', u''),
                    'coupon_click_url': coupon_click_link,
                    'click_url': click_link,
                    'memo': item.get(u'备注', u'')
                })
            except Exception as e:
                print item_id
                print e
                continue

        _split_fname = '{}.{}.json'.format(fname, loop)
        _split_path = os.path.join(output_dir, _split_fname)
        if output_farg:
            print '----------->', loop, _split_fname
            with open(_split_path, 'w') as outfile:
                json.dump(output_farg, outfile)
            loop += 1
        else:
            print '-----------> empty chunk ...'
