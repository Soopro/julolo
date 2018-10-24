# coding=utf-8
from __future__ import absolute_import

from flask import current_app

from utils.response import output_json

from helpers.common import connect_taoke

from ..errors import StoreItemDetailsError


@output_json
def get_item_details(item_id):

    item = current_app.mongodb.Commodity.find_one_by_itemid(item_id)

    if not item:
        return []
    elif item['details']:
        return item['details']

    taoke = connect_taoke()

    try:
        details = taoke.item_details(item_id)
    except Exception as e:
        current_app.logger.error(StoreItemDetailsError(e))
        details = []
    try:
        item['details'] = details
        item.save()
    except Exception as e:
        current_app.logger.error(StoreItemDetailsError(e))

    return details
