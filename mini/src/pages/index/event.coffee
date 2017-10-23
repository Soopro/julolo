core = require('../../core.js')
restStore = require('../../restapi/store.js')

app = getApp()

Page
  data:
    image: core.image
    is_loading: null
    has_more: null
    coupons: []
    evt: null
    has_cart: false

  paged: 1
  perpage: 60
  limit: 100

  # lifecycle
  onShareAppMessage: app.share

  onLoad: (opts)->
    self = @
    restStore.evt.get opts.evt
    .then (evt)->
      self.setData
        evt: evt
    .then ->
      self.list_event()

  onShow: ->
    self = @
    self.setData
      has_cart: app.cart.len() > 0

  onPullDownRefresh: ->
    self = @
    self.paged = 1
    self.setData
      coupons: []
      has_more: null
    self.list_event()
    .finally ->
      wx.stopPullDownRefresh()

  onReachBottom: ->
    self = @
    if self.data.has_more is true
      self.paged += 1
      self.list_event()


  # hanlders
  list_event: ->
    self = @
    self.setData
      is_loading: true
    evt_slug = self.data.evt.slug
    restStore.evt.items evt_slug,
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

  go_cart: app.go_cart
