# coding=utf-8
from __future__ import absolute_import

import csv


def load_csv(csv_path):
    sheetdata = []
    with open(csv_path, 'rb') as csvfile:
        readered = csv.reader(csvfile)
        labels = None
        for row in readered:
            if not labels:
                labels = row
                continue
            row_data = {}
            try:
                for idx, item in enumerate(row):
                    label = labels[idx]
                    if isinstance(label, str):
                        label = label.decode('utf-8')
                    if isinstance(item, str):
                        item = item.decode('utf-8')
                    label = label.split('(')[0]  # remove all `(...)`
                    row_data[label] = item
            except Exception as e:
                print 'Load CSV Error: --------->'
                print e
                continue
            sheetdata.append(row_data)

    return sheetdata
