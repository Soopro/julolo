# coding=utf-8
from .controllers import *

urlpatterns = [
    # store
    ('', get_store, 'GET'),

    # coupon
    ('/coupon', list_coupons, 'GET'),
    ('/coupon', search_coupons, 'POST'),

    # category
    ('/category', list_categories, 'GET'),
    ('/category/<cat_id>', get_cat_coupons, 'GET'),

    # promotion
    ('/promotion', list_promotions, 'GET'),
    ('/ad/<ad_slot>', get_advertising, 'GET'),


    # tips
    ('/tip', list_tips, 'GET'),

]
