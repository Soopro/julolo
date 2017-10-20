# coding=utf-8
from .controllers import *

urlpatterns = [
    # store
    ('', get_store, 'GET'),

    # coupon
    ('/coupon', list_coupons, 'GET'),
    ('/coupon', search_coupons, 'POST'),
    ('/coupon/code', generate_coupon_code, 'POST'),

    # category
    ('/category', list_categories, 'GET'),
    ('/category/<cat_slug>', get_category, 'GET'),

    # promotion
    ('/promotion', list_promotions, 'GET'),
    ('/promotion/<promo_slug>', get_promotion, 'GET'),
    ('/promotion/<promo_slug>/items', list_promotion_items, 'GET'),

    # event
    ('/event', list_events, 'GET'),
    ('/event/<evt_slug>', get_event, 'GET'),
    ('/event/<evt_slug>/items', list_event_items, 'GET'),

    # tips
    ('/tip', list_tips, 'GET'),

]
