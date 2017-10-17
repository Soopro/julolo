# coding=utf-8
from .controllers import *

urlpatterns = [
    # coupon
    ('/coupon', list_coupons, 'GET'),
    ('/coupon', search_coupons, 'POST'),
]
