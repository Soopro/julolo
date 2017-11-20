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


class StoreCommodityNotFound(NotFound):
    response_code = 800004
    status_message = 'STORE_COMMODITY_NotFound'


class StoreCategoryNotFound(NotFound):
    response_code = 800005
    status_message = 'STORE_CATEGORY_NOT_FOUND'


class StoreCategoryInvalid(InternalServerError):
    response_code = 800006
    status_message = 'STORE_CATEGORY_INVALID'


class StorePromoNotFound(NotFound):
    response_code = 800007
    status_message = 'STORE_PROMOTION_NOT_FOUND'


class StorePromoItemsError(NotFound):
    response_code = 800008
    status_message = 'STORE_PROMOTION_ITEMS_ERROR'


class StoreActivityNotFound(NotFound):
    response_code = 800009
    status_message = 'STORE_EVENT_NOT_FOUND'


class StoreActivityItemsError(NotFound):
    response_code = 800010
    status_message = 'STORE_EVENT_ITEMS_ERROR'


class StoreItemDetailsError(NotFound):
    response_code = 800020
    status_message = 'STORE_ITEM_DETAILS_ERROR'
