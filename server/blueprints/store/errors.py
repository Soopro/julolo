# coding=utf-8
from __future__ import absolute_import

from apiresps.errors import (NotFound,
                             InternalServerError)


class StoreNotFound(NotFound):
    response_code = 800001
    status_message = 'STORE_NOT_FOUND'


class StoreCouponError(InternalServerError):
    response_code = 800002
    status_message = 'STORE_COUPON_ERROR'
