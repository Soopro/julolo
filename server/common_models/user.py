# coding=utf-8
from __future__ import absolute_import

from utils.models import BaseDocument
from utils.misc import now
from mongokit import ObjectId, INDEX_DESCENDING
import re


class User(BaseDocument):
    STATUS_DEACTIVATED, STATUS_ACTIVATED, STATUS_BANNED = (0, 1, 2)
    GENDER = (0, 1, 2)

    structure = {
        'login': unicode,
        'password_hash': unicode,
        'slug': unicode,
        'meta': dict,
        'creation': int,
        'updated': int,
        'status': int,
        'deleted': int,
    }
    sensitive_fields = ['meta']
    required_fields = ['login', 'slug', 'password_hash']
    default_values = {
        'meta': {},
        'creation': now,
        'updated': now,
        'deleted': 0,
        'status': STATUS_DEACTIVATED
    }
    indexes = [
        {
            'fields': ['login'],
            'unique': True,
        },
        {
            'fields': ['slug'],
            'unique': True,
        },
        {
            'fields': ['creation'],
        },
        {
            'fields': ['deleted'],
        }
    ]

    def find_alive(self, login=None, slug=None):
        _query = {
            'deleted': 0,
        }
        if isinstance(login, unicode):
            re_login = re.compile(ur'.*{}.*'.format(login), re.IGNORECASE)
            _query.update({'login': re_login})
        if isinstance(slug, unicode):
            re_slug = re.compile(ur'.*{}.*'.format(slug), re.IGNORECASE)
            _query.update({'slug': re_slug})
        return self.find(_query).sort('creation', INDEX_DESCENDING)

    def find_dead(self, login=None, slug=None):
        _query = {
            'deleted': 1,
        }
        if isinstance(login, unicode):
            re_login = re.compile(ur'.*{}.*'.format(login), re.IGNORECASE)
            _query.update({'login': re_login})
        if isinstance(slug, unicode):
            re_slug = re.compile(ur'.*{}.*'.format(slug), re.IGNORECASE)
            _query.update({'slug': re_slug})
        return self.find(_query)

    def find_one_by_id(self, user_id):
        return self.find_one({
            '_id': ObjectId(user_id),
            'deleted': 0,
        })

    def find_one_dead_by_id(self, user_id):
        return self.find_one({
            '_id': ObjectId(user_id),
            'deleted': 1,
        })

    def find_one_by_slug(self, slug):
        return self.find_one({
            'slug': slug,
            'deleted': 0,
        })

    def find_one_by_login(self, login):
        return self.find_one({
            'login': login,
            'deleted': 0,
        })

    def find_by_ids(self, ids):
        return self.find({
            '_id': {'$in': [ObjectId(_id) for _id in ids
                            if ObjectId.is_valid(_id)]},
            'deleted': 0,
        }).limit(120)

    def count_used(self):
        return self.find({
            'deleted': 0,
        }).count()

    def remove(self):
        self['login'] = u'.{}.{}'.format(self['login'], self['_id'])
        self['slug'] = u'.{}.{}'.format(self['slug'], self['_id'])
        self['updated'] = now()
        self['deleted'] = 1
        self.save()
        return self['_id']


class Property(BaseDocument):

    structure = {
        'user_id': ObjectId,
        'app_key': unicode,
        'app_secret': unicode,
        'pid': unicode,
        'creation': int,
        'updated': int,
    }
    required_fields = ['user_id', 'app_key', 'app_secret']
    default_values = {
        'pid': u'',
        'creation': now,
        'updated': now,
    }
    indexes = [
        {
            'fields': ['user_id'],
            'unique': True,
        }
    ]

    def find_one_by_uid(self, user_id):
        return self.find_one({
            'user_id': ObjectId(user_id),
        })

    def clear(self, user_id):
        return self.collection.remove({
            'user_id': ObjectId(user_id),
        })
