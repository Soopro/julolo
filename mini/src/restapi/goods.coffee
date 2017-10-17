requests = require('requests.js')

list_coupons = (opts)->
  requests.get('/goods/coupon', opts)


search_coupons = (opts)->
  requests.post('/goods/coupon', opts)


module.exports =
  coupon:
    list: list_coupons
    search: search_coupons
