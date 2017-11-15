# coding=utf-8
from __future__ import absolute_import

from mongokit import DocumentMigration


class PromotionMigration(DocumentMigration):

    def allmigration01_add_splash(self):
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
