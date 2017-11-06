# coding=utf-8
from __future__ import absolute_import

from mongokit import DocumentMigration


class CategoryMigration(DocumentMigration):

    def allmigration01_remove_complete(self):
        self.target = {'pic': {'$exists': False}}
        if not self.status:
            self.update = {
                '$set': {
                    'pic': u''
                }
            }
            self.collection.update(self.target,
                                   self.update,
                                   multi=True,
                                   safe=True)
