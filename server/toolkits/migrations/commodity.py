# coding=utf-8
from __future__ import absolute_import

from mongokit import DocumentMigration


class CommodityMigration(DocumentMigration):

    def allmigration01_rename_favorite_key(self):
        self.target = {'favorite_key': {'$exists': True}}
        if not self.status:
            self.update = {
                '$rename': {
                    'favorite_key': 'activity'
                }
            }
            self.collection.update(self.target,
                                   self.update,
                                   multi=True,
                                   safe=True)

    # def allmigration02_add_memo(self):
    #     self.target = {'memo': {'$exists': False}}
    #     if not self.status:
    #         self.update = {
    #             '$set': {
    #                 'memo': u''
    #             }
    #         }
    #         self.collection.update(self.target,
    #                                self.update,
    #                                multi=True,
    #                                safe=True)

    # def allmigration04_add_coupon_id(self):
    #     self.target = {'coupon_id': {'$exists': False}}
    #     if not self.status:
    #         self.update = {
    #             '$set': {
    #                 'coupon_id': u''
    #             }
    #         }
    #         self.collection.update(self.target,
    #                                self.update,
    #                                multi=True,
    #                                safe=True)

    # def allmigration05_add_coupon_url(self):
    #     self.target = {'coupon_url': {'$exists': False}}
    #     if not self.status:
    #         self.update = {
    #             '$set': {
    #                 'coupon_url': u''
    #             }
    #         }
    #         self.collection.update(self.target,
    #                                self.update,
    #                                multi=True,
    #                                safe=True)
