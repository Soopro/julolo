# coding=utf-8
from __future__ import absolute_import

import os
import csv
import json


def _convert_unicode(input):
        if not isinstance(input, unicode):
            return input.decode('utf-8')
        else:
            return input


def load_commodities(csv_path):
    commodities = []
    with open(csv_path, 'rb') as csvfile:
        readered = csv.reader(csvfile)
        for row in readered:
            try:
                item_id = int(row[0])
            except Exception:
                continue

            commodities.append({
                'item_id': item_id,
                'title': _convert_unicode(row[1]),
                'src': _convert_unicode(row[2]),
                'detail_url': _convert_unicode(row[3]),
                'category_name': _convert_unicode(row[4]),
                'click_url': _convert_unicode(row[5]),
                'price': float(row[6]),
                'volume': int(row[7]),
                'income_rate': float(row[8]),
                'commission': float(row[9]),
                'seller_im': _convert_unicode(row[10]),
                'seller_id': _convert_unicode(row[11]),
                'shop': _convert_unicode(row[12]),
                'type': _convert_unicode(row[13]),
                'coupon_id': _convert_unicode(row[14]),
                'coupon_volume': int(row[15]),
                'coupon_remine': int(row[16]),
                'coupon': _convert_unicode(row[17]),
                'start_time': _convert_unicode(row[18]),
                'end_time': _convert_unicode(row[19]),
                'coupon_url': _convert_unicode(row[20]),
                'coupon_click_url': _convert_unicode(row[21]),
            })

    return commodities


def output_commodities(commodities, output_path):
    with open(output_path, 'w') as outfile:
        json.dump(commodities, outfile)


def convert(csv_path, output_path=None):
    fname, ext = os.path.splitext(csv_path)
    if not os.path.isfile(csv_path) or ext != '.csv':
        raise Exception('Invalid file, must be .csv')
    if not output_path:
        output_path = '{}{}'.format(fname, '.json')
    commodities = load_commodities(csv_path)
    output_commodities(commodities, output_path)
