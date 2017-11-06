requests = require('requests.js')

get_store = (opts)->
  requests.get('/store', opts)

list_commodities = (opts)->
  requests.get('/store/commodity', opts)

search_commodities = (opts)->
  requests.post('/store/commodity', opts)

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

list_tips = (opts)->
  requests.get('/store/tip', opts)


module.exports =
  store:
    get: get_store
  commodity:
    list: list_commodities
    search: search_commodities
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
