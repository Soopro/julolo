# coding=utf-8
from __future__ import absolute_import
import time


class Analyzer(object):

    TOTAL_CUSTOMER_KEY = 'anlys.customer.total'
    DAY_CUSTOMER_KEY_PREFIX = 'anlys.customer.day:'

    expires = 3600 * 24 * 7

    def __init__(self, rds_read, rds_write=None, expires=None):
        self.rds_read = rds_read
        self.rds_write = rds_write or rds_read

        if expires:
            self.expires = int(expires)

    def get_customer(self):
        redis = self.rds_read
        total = redis.get(self.TOTAL_CUSTOMER_KEY) or 0

        key_pattern = '{}*'.format(self.DAY_CUSTOMER_KEY_PREFIX)
        days = redis.keys(key_pattern)
        day_list = [{
            'date': day.split(self.DAY_CUSTOMER_KEY_PREFIX)[-1],
            'count': redis.get(day)
        } for day in days]

        return {
            'total': total,
            'days': day_list,
        }

    def record_customer(self):
        today = time.strftime('%Y-%m-%d')
        day_customer_key = '{}{}'.format(self.DAY_CUSTOMER_KEY_PREFIX, today)

        redis = self.rds_write

        pip = redis.pipeline(transaction=False)

        # customer
        pip.incr(self.TOTAL_CUSTOMER_KEY)
        pip.incr(day_customer_key)
        pip.expire(day_customer_key, self.expires)

        pip.execute()

        return True
