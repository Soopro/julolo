# coding=utf-8
from __future__ import absolute_import

from apiresps.errors import InternalServerError


class CouponRemoteError(InternalServerError):
    response_code = 800001
    status_message = 'COUPON_REMOTE_ERROR'
