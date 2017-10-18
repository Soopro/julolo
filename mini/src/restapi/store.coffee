requests = require('requests.js')

get_store = (opts)->
  requests.get('/store', opts)

list_coupons = (opts)->
  requests.get('/store/coupon', opts)

search_coupons = (opts)->
  requests.post('/store/coupon', opts)

list_categories = (opts)->
  requests.get('/store/category', opts)

get_category = (cat_id, opts)->
  requests.get('/store/category/'+cat_id, opts)

list_promotions = (opts)->
  requests.get('/store/promotion', opts)


module.exports =
  info: get_store
  promotion:
    list: list_promotions
  category:
    list: list_categories
    get: get_category
  coupon:
    list: list_coupons
    search: search_coupons

