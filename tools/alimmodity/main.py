# coding=utf-8
from __future__ import absolute_import

import os
import json

from .csv import load_csv
from .xls import load_xls


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


def _convert_shop_type(input_type):
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
        output_data = []
        for item in farg_data:
            try:
                item_id = int(item.get(u'商品id'))
                category = item.get(u'商品一级类目')
                cid = int(policy['category'].get(category, -1))
                output_data.append({
                    'item_id': item_id,
                    'title': item.get(u'商品名称'),
                    'pic_url': item.get(u'商品主图'),
                    'detail_url': item.get(u'商品详情页链接地址'),
                    'category': category,
                    'cid': cid,
                    'click_url': item.get(u'淘宝客链接'),
                    'price': float(item.get(u'商品价格')),
                    'volume': int(item.get(u'商品月销量')),
                    'income_rate': float(item.get(u'收入比率')),
                    'commission': float(item.get(u'佣金')),
                    'seller_im': item.get(u'卖家旺旺'),
                    'seller_id': item.get(u'卖家id'),
                    'shop_title': item.get(u'店铺名称'),
                    'shop_type': _convert_shop_type(item.get(u'平台类型')),
                    'coupon_id': item.get(u'优惠券id'),
                    'coupon_volume': int(item.get(u'优惠券总量')),
                    'coupon_remine': int(item.get(u'优惠券剩余量')),
                    'coupon_info': item.get(u'优惠券面额'),
                    'coupon_start_time': item.get(u'优惠券开始时间'),
                    'coupon_end_time': item.get(u'优惠券结束时间'),
                    'coupon_url': item.get(u'优惠券链接'),
                    'coupon_click_url': item.get(u'商品优惠券推广链接'),
                })
            except Exception as e:
                print e
                continue

        _split_fname = '{}.{}.json'.format(fname, loop)
        _split_path = os.path.join(output_dir, _split_fname)
        print '----------->', loop, _split_fname

        with open(_split_path, 'w') as outfile:
            json.dump(output_data, outfile)
        loop += 1
