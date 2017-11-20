# coding=utf-8
from __future__ import absolute_import

from mongokit import DocumentMigration


class PromotionMigration(DocumentMigration):
    def allmigration01_remove_favorite_key(self):
        self.target = {'favorite_key': {'$exists': True}}
        if not self.status:
            self.update = {
                '$unset': {
                    'favorite_key': None
                }
            }
            self.collection.update(self.target,
                                   self.update,
                                   multi=True,
                                   safe=True)
