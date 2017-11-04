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

    def allmigration02_remove_allow_tpwd(self):
        self.target = {'allow_tpwd': {'$exists': True}}
        if not self.status:
            self.update = {
                '$unset': {
                    'allow_tpwd': False
                }
            }
            self.collection.update(self.target,
                                   self.update,
                                   multi=True,
                                   safe=True)

    def allmigration03_remove_tpwd_msg(self):
        self.target = {'tpwd_msg': {'$exists': True}}
        if not self.status:
            self.update = {
                '$unset': {
                    'tpwd_msg': False
                },
                '$set': {
                    'tpwd': u'',
                }
            }
            self.collection.update(self.target,
                                   self.update,
                                   multi=True,
                                   safe=True)
