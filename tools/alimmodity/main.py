# coding=utf-8
from __future__ import absolute_import

import os
import csv
import json


def _load_policy(policy_path):
    _policy = {
        'size': 500,
        'category': {},
    }
    print policy_path
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


def _convert_unicode(input):
    if not isinstance(input, unicode):
        return input.decode('utf-8')
    else:
        return input


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


def load_csv(csv_path, policy={}):
    commodities = []
    with open(csv_path, 'rb') as csvfile:
        readered = csv.reader(csvfile)
        for row in readered:
            try:
                item_id = int(row[0])
                if policy.get('category'):
                    cat_name = _convert_unicode(row[4])
                    cid = int(policy['category'].get(cat_name))
                else:
                    cid = -1  # unknow category id.
            except Exception:
                continue

            commodities.append({
                'item_id': item_id,
                'title': _convert_unicode(row[1]),
                'pic_url': _convert_unicode(row[2]),
                'detail_url': _convert_unicode(row[3]),
                'category': _convert_unicode(row[4]),
                'cid': cid,
                'click_url': _convert_unicode(row[5]),
                'price': float(row[6]),
                'volume': int(row[7]),
                'income_rate': float(row[8]),
                'commission': float(row[9]),
                'seller_im': _convert_unicode(row[10]),
                'seller_id': _convert_unicode(row[11]),
                'shop_name': _convert_unicode(row[12]),
                'shop_type': _convert_shop_type(row[13]),
                'coupon_id': _convert_unicode(row[14]),
                'coupon_volume': int(row[15]),
                'coupon_remine': int(row[16]),
                'coupon_info': _convert_unicode(row[17]),
                'coupon_start_time': _convert_unicode(row[18]),
                'coupon_end_time': _convert_unicode(row[19]),
                'coupon_url': _convert_unicode(row[20]),
                'coupon_click_url': _convert_unicode(row[21]),
            })

    return commodities


def convert(csv_path, output_dir=None, policy_path=None):
    fname, ext = os.path.splitext(csv_path)
    if not os.path.isfile(csv_path) or ext != '.csv':
        raise Exception('Invalid file, must be .csv')

    if not output_dir:
        output_dir = fname
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    policy = _load_policy(policy_path)

    split_size = min(max(_parse_int(policy['size']), 100), 10000)

    commodities = load_csv(csv_path, policy)
    loop = 1

    for splited in _chunks(commodities, split_size):
        _split_fname = '{}.{}.json'.format(fname, loop)
        _split_path = os.path.join(output_dir, _split_fname)
        print '----------->', loop, _split_fname

        with open(_split_path, 'w') as outfile:
            json.dump(splited, outfile)
        loop += 1
