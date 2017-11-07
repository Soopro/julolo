# coding=utf-8
from __future__ import absolute_import

from mongokit import DocumentMigration


class CategoryMigration(DocumentMigration):

    def allmigration01_rename_pic_to_poster(self):
        self.target = {'pic': {'$exists': True}}
        if not self.status:
            self.update = {
                '$rename': {
                    'pic': 'poster'
                }
            }
            self.collection.update(self.target,
                                   self.update,
                                   multi=True,
                                   safe=True)
