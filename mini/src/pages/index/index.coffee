core = require('../../core.js')
restStore = require('../../restapi/store.js')

app = getApp()

Page
  data:
    image: core.image
    is_loading: null
    has_more: null
    coupons: []
    events: []
    promotions: []
    categories: []
    banners: []

  paged: 1
  perpage: 60
  limit: 100

  # lifecycle
  onShareAppMessage: app.share

  onLoad: (opts)->
    self = @
    restStore.evt.list()
    .then (events)->
      self.setData
        events: events
    .then ->
      restStore.promotion.list()
    .then (promotions)->
      self.setData
        promotions: promotions
    .then ->
      restStore.category.list()
    .then (categories)->
      self.setData
        categories: categories
    .then ->
      self.list()

  onPullDownRefresh: ->
    self = @
    self.paged = 1
    self.setData
      coupons: []
      has_more: null
    self.list()
    .finally ->
      wx.stopPullDownRefresh()

  onReachBottom: ->
    self = @
    if self.data.has_more is true
      self.paged += 1
      self.list()


  # hanlders
  list: ->
    self = @
    self.setData
      is_loading: true
    restStore.newest.list
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

  enter_event: (e)->
    evt = e.currentTarget.dataset.evt
    app.goto
      route: '/pages/index/event'
      query:
        evt: evt.slug

  enter_promo: (e)->
    promo = e.currentTarget.dataset.promo
    app.goto
      route: '/pages/index/promotion'
      query:
        promo: promo.slug

  enter_category: (e)->
    cat = e.currentTarget.dataset.category
    app.goto
      route: '/pages/index/category'
      query:
        cat: cat.slug

  enter: (e)->
    item = e.currentTarget.dataset.item
    return if not item
    app.g.current_item = item
    wx.setStorageSync('item', item)
    app.goto
      route: '/pages/index/item'
