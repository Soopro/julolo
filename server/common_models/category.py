# coding=utf-8
from __future__ import absolute_import

from utils.models import BaseDocument
from utils.misc import now
from document import ObjectId, INDEX_DESC, INDEX_ASC


class Category(BaseDocument):
    STATUS_OFF, STATUS_ON = 0, 1

    MAX_STORAGE = 600
    MAX_QUERY = 60

    structure = {
        'user_id': ObjectId,
        'slug': unicode,
        'cat_ids': [unicode],
        'label': unicode,
        'icon': unicode,
        'priority': int,
        'status': int,
        'updated': int,
        'creation': int
    }
    sensitive_fields = ['label']
    required_fields = ['user_id', 'slug']
    default_values = {
        'label': u'',
        'icon': u'',
        'priority': 0,
        'creation': now,
        'updated': now,
    }
    indexes = [
        {
            'fields': ['user_id', 'slug'],
            'unique': True,
        },
        {
            'fields': [('priority', INDEX_ASC), ('updated', INDEX_DESC)],
        },
        {
            'fields': ['status'],
        },
    ]

    def find_one_by_id(self, _id):
        return self.find_one({
            '_id': ObjectId(_id),
        })

    def find_one_by_uid_slug(self, user_id, slug):
        return self.find_one({
            'user_id': ObjectId(user_id),
            'slug': slug
        })

    def find_by_uid(self, user_id):
        sorts = [('priority', INDEX_ASC), ('updated', INDEX_DESC)]
        return self.find({
            'user_id': ObjectId(user_id),
        }).sort(sorts).limit(self.MAX_QUERY)

    def find_active_by_uid(self, user_id):
        sorts = [('priority', INDEX_ASC), ('updated', INDEX_DESC)]
        return self.find({
            'user_id': ObjectId(user_id),
            'status': self.STATUS_ON,
        }).sort(sorts).limit(self.MAX_QUERY)

    def clear(self, user_id):
        return self.collection.remove({
            'user_id': ObjectId(user_id),
        })
