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
    ('/banner/<slot>', get_banner, 'GET'),


    # tips
    ('/tip', list_tips, 'GET'),

]
