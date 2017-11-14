# coding=utf-8
from __future__ import absolute_import

from mongokit import DocumentMigration


class StoreMigration(DocumentMigration):
    def allmigration01_remove_cat_ids(self):
        self.target = {'cat_ids': {'$exists': True}}
        if not self.status:
            self.update = {
                '$unset': {
                    'cat_ids': False
                }
            }
            self.collection.update(self.target,
                                   self.update,
                                   multi=True,
                                   safe=True)

    def allmigration02_remove_event_limit(self):
        self.target = {'event_limit': {'$exists': True}}
        if not self.status:
            self.update = {
                '$unset': {
                    'event_limit': False
                }
            }
            self.collection.update(self.target,
                                   self.update,
                                   multi=True,
                                   safe=True)

    def allmigration03_remove_promo_limit(self):
        self.target = {'promotion_limit': {'$exists': True}}
        if not self.status:
            self.update = {
                '$unset': {
                    'promotion_limit': False
                }
            }
            self.collection.update(self.target,
                                   self.update,
                                   multi=True,
                                   safe=True)

    def allmigration04_add_splash(self):
        self.target = {'splash': {'$exists': False}}
        if not self.status:
            self.update = {
                '$set': {
                    'splash': u''
                }
            }
            self.collection.update(self.target,
                                   self.update,
                                   multi=True,
                                   safe=True)

    def allmigration05_add_status(self):
        self.target = {'status': {'$exists': False}}
        if not self.status:
            self.update = {
                '$set': {
                    'status': 1
                }
            }
            self.collection.update(self.target,
                                   self.update,
                                   multi=True,
                                   safe=True)

    def allmigration06_add_title(self):
        self.target = {'title': {'$exists': False}}
        if not self.status:
            self.update = {
                '$set': {
                    'title': u''
                }
            }
            self.collection.update(self.target,
                                   self.update,
                                   multi=True,
                                   safe=True)

    def allmigration07_add_default(self):
        self.target = {'default': {'$exists': False}}
        if not self.status:
            self.update = {
                '$set': {
                    'default': u''
                }
            }
            self.collection.update(self.target,
                                   self.update,
                                   multi=True,
                                   safe=True)
