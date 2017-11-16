# coding=utf-8
from __future__ import absolute_import

from mongokit import DocumentMigration


class StoreMigration(DocumentMigration):

    def allmigration01_remove_high(self):
        self.target = {'high_commission': {'$exists': True}}
        if not self.status:
            self.update = {
                '$unset': {
                    'high_commission': False,
                }
            }
            self.collection.update(self.target,
                                   self.update,
                                   multi=True,
                                   safe=True)

    def allmigration02_add_sort_type(self):
        self.target = {'sort_type': {'$exists': False}}
        if not self.status:
            self.update = {
                '$set': {
                    'sort_type': 0,
                }
            }
            self.collection.update(self.target,
                                   self.update,
                                   multi=True,
                                   safe=True)
