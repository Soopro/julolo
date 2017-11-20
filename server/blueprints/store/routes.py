# coding=utf-8
from .controllers import *

urlpatterns = [
    # store
    ('', get_store, 'GET'),

    # commodity
    ('/commodity', list_commodities, 'GET'),
    ('/commodity', search_commodities, 'POST'),
    ('/commodity/<co_id>', get_commodity, 'GET'),

    # coupon
    ('/coupon', list_item_coupons, 'GET'),
    ('/coupon', search_item_coupons, 'POST'),
    ('/coupon/code', generate_coupon_code, 'POST'),

    # details
    ('/details', get_item_details, 'GET'),

    # category
    ('/category', list_categories, 'GET'),
    ('/category/<cat_slug>', get_category, 'GET'),

    # promotion
    ('/promotion', list_promotions, 'GET'),
    ('/promotion/<promo_slug>', get_promotion, 'GET'),
    ('/promotion/<promo_slug>/items', list_promotion_items, 'GET'),

    # event
    ('/shortcut', list_shortcuts, 'GET'),
    ('/shortcut/<shortcut_slug>', get_shortcut, 'GET'),

    # tips
    ('/tip', list_tips, 'GET'),

]
