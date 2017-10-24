# coding=utf-8
from __future__ import absolute_import
import time


class Analyzer(object):

    TOTAL_CUSTOMER_KEY = 'anlys.customer.total'
    DAY_CUSTOMER_KEY_PREFIX = 'anlys.customer.day:'

    expires = 3600 * 24 * 7

    def __init__(self, rds_write, rds_read, expires=None):
        self.rds_write = rds_write
        self.rds_read = rds_read

        if expires:
            self.expires = int(expires)

    def get_total_customer(self):
        redis = self.rds_read
        count = redis.get(self.TOTAL_CUSTOMER_KEY) or 0
        return {
            'total': count
        }

    def get_days_customer(self):
        redis = self.rds_read
        days = redis.keys(self.DAY_CUSTOMER_KEY_PREFIX)
        day_list = []
        for day in days:
            day_list.append({
                'day': day.split(self.DAY_CUSTOMER_KEY_PREFIX)[-1],
                'count': redis.get(day)
            })
        return day_list

    def record_customer(self):
        today = time.strftime('%Y-%m-%d')
        day_customer_key = '{}{}'.format(self.DAY_CUSTOMER_KEY_PREFIX, today)

        redis = self.rds_write

        pip = redis.pipeline(transaction=False)

        # customer
        pip.incr(self.KEY_TOTAL_CUSTOMER)
        pip.incr(day_customer_key)
        pip.expire(day_customer_key, self.expires)

        pip.execute()

        total_count = redis.get(self.KEY_TOTAL_CUSTOMER)
        today_count = redis.get(day_customer_key)
        return {
            'total': total_count,
            'today': today_count,
        }
