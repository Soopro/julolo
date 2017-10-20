requests = require('requests.js')

list_coupons = (opts)->
  requests.get('/store/coupon', opts)

search_coupons = (opts)->
  requests.post('/store/coupon', opts)

create_coupon_code = (opts)->
  requests.post('/store/coupon/code', opts)

list_categories = (opts)->
  requests.get('/store/category', opts)

get_category = (cat_slug, opts)->
  requests.get('/store/category/'+cat_slug, opts)

list_promotions = (opts)->
  requests.get('/store/promotion', opts)

get_promotion = (promo_slug, opts)->
  requests.get('/store/promotion/'+promo_slug, opts)

list_promotion_items = (promo_slug, opts)->
  requests.get('/store/promotion/'+promo_slug+'/items', opts)

list_events = (opts)->
  requests.get('/store/event', opts)

get_event = (event_slug, opts)->
  requests.get('/store/event/'+event_slug, opts)

list_event_items = (event_slug, opts)->
  requests.get('/store/event/'+event_slug+'/items', opts)

list_tips = (opts)->
  requests.get('/store/tip', opts)


module.exports =
  evt:
    list: list_events
    get: get_event
    items: list_event_items
  promotion:
    list: list_promotions
    get: get_promotion
    items: list_promotion_items
  category:
    list: list_categories
    get: get_category
  coupon:
    list: list_coupons
    search: search_coupons
    code: create_coupon_code
  tip:
    list: list_tips