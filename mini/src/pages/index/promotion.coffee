core = require('../../core.js')
utils = require('../../utils.js')
restStore = require('../../restapi/store.js')

app = getApp()

Page
  data:
    image: core.image
    is_loading: null
    has_more: null
    commodities: []
    promotion: null

  paged: 1
  perpage: 12
  timestamp: utils.now()

  # lifecycle
  onShareAppMessage: app.share

  onLoad: (opts)->
    self = @
    restStore.promotion.get opts.slug
    .then (promotion)->
      self.setData
        promotion: promotion
    .then ->
      self.list_promo()

  onPullDownRefresh: ->
    self = @
    self.paged = 1
    self.timestamp = utils.now()
    self.setData
      commodities: []
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
        item.coupon = app.parse_coupon(item.coupon_info)
      self.setData
        commodities: self.data.commodities.concat(results)
        has_more: results[0] and results[0]._more
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

