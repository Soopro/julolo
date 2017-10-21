# coding=utf-8
from __future__ import absolute_import

from utils.models import BaseDocument
from utils.misc import now

from document import ObjectId


class Store(BaseDocument):

    structure = {
        'app_key': unicode,
        'app_secret': unicode,
        'pid': unicode,
        'ssl': bool,
        'allow_tkl': bool,
        'creation': int,
        'updated': int,
    }
    required_fields = ['app_key', 'app_secret', 'pid']
    default_values = {
        'ssl': False,
        'allow_tkl': False,
        'creation': now,
        'updated': now,
    }
    indexes = [
        {
            'fields': ['app_key'],
            'unique': True,
        }
    ]

    def find_one_by_id(self, _id):
        return self.find_one({
            '_id': ObjectId(_id),
        })
