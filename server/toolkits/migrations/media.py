# coding=utf-8
from __future__ import absolute_import

from mongokit import DocumentMigration


class MediaMigration(DocumentMigration):
    pass

    # def allmigration01_remove_complete(self):
    #     self.target = {'verification': {'$exists': True}}
    #     if not self.status:
    #         self.update = {
    #             '$unset': {
    #                 'verification': False
    #             },
    #             '$set': {
    #                 'verified': False
    #             }
    #         }
    #         self.collection.update(self.target,
    #                                self.update,
    #                                multi=True,
    #                                safe=True)
