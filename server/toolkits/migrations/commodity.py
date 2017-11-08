# coding=utf-8
from __future__ import absolute_import

from mongokit import DocumentMigration


class CommodityMigration(DocumentMigration):
    def allmigration01_add_favorite_key(self):
        self.target = {'favorite_key': {'$exists': False}}
        if not self.status:
            self.update = {
                '$set': {
                    'favorite_key': u''
                }
            }
            self.collection.update(self.target,
                                   self.update,
                                   multi=True,
                                   safe=True)

    def allmigration01_add_memo(self):
        self.target = {'memo': {'$exists': False}}
        if not self.status:
            self.update = {
                '$set': {
                    'memo': u''
                }
            }
            self.collection.update(self.target,
                                   self.update,
                                   multi=True,
                                   safe=True)
