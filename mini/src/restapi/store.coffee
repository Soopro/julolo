requests = require('requests.js')

list_coupons = (opts)->
  requests.get('/store/coupon', opts)

search_coupons = (opts)->
  requests.post('/store/coupon', opts)

create_coupon_code = (opts)->
  requests.post('/store/coupon/code', opts)

list_categories = (opts)->
  requests.get('/store/category', opts)

get_category = (cat_id, opts)->
  requests.get('/store/category/'+cat_id, opts)

list_promotions = (opts)->
  requests.get('/store/promotion', opts)

list_tips = (opts)->
  requests.get('/store/tip', opts)

get_home_banner = (opts)->
  requests.get('/store/banner/home', opts)


module.exports =
  tip:
    list: list_tips
  promotion:
    list: list_promotions
  category:
    list: list_categories
    get: get_category
  coupon:
    list: list_coupons
    search: search_coupons
    code: create_coupon_code
  banner:
    home: get_home_banner
