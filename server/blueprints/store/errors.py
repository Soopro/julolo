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


class StoreCouponGenerateFailed(InternalServerError):
    response_code = 800003
    status_message = 'STORE_COUPON_GENERATE_FAILED'


class StoreGoodsError(InternalServerError):
    response_code = 800004
    status_message = 'STORE_GOODS_ERROR'
