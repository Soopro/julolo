core = require('../../core.js')
restStore = require('../../restapi/store.js')

app = getApp()

Page
  data:
    image: core.image
    is_loading: null
    has_more: null
    coupons: []
    promotion: null

  paged: 1
  perpage: 100
  limit: 6

  # lifecycle
  onShareAppMessage: app.share

  onLoad: (opts)->
    self = @
    restStore.promotion.get opts.promo
    .then (promotion)->
      self.setData
        promotion: promotion
    .then ->
      self.list_promo()

  onPullDownRefresh: ->
    self = @
    self.paged = 1
    self.setData
      coupons: []
      has_more: null
    self.list_promo()
    .finally ->
      wx.stopPullDownRefresh()

  onReachBottom: ->
    self = @
    if self.data.has_more is true
      self.paged += 1
      self.list_promo()


  # hanlders
  list_promo: ->
    self = @
    self.setData
      is_loading: true
    promo_slug = self.data.promotion.slug
    restStore.promotion.items promo_slug,
      data:
        paged: self.paged
        perpage: self.perpage
    .then (results)->
      for item in results
        item.coupon = app.parse_coupon(item.coupon)
      self.setData
        coupons: self.data.coupons.concat(results)
        has_more: results.length >= self.perpage and self.paged < self.limit
    .finally ->
      self.setData
        is_loading: false

  enter: (e)->
    item = e.currentTarget.dataset.item
    return if not item
    app.g.current_item = item
    wx.setStorageSync('item', item)
    app.goto
      route: '/pages/index/item'