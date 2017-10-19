core = require('../../core.js')
restStore = require('../../restapi/store.js')

app = getApp()

Page
  data:
    image: core.image
    is_loading: null
    has_more: null
    coupons: []
    promotions: []
    categories: []
    banner: null

  paged: 1
  perpage: 12

  # lifecycle
  onShareAppMessage: app.share

  onLoad: (opts)->
    self = @
    app.goto
      route: '/pages/user/user'
      method: wx.switchTab
    return
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
      restStore.banner.home()
    .then (banner)->
      self.setData
        banner: banner
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
    restStore.coupon.list
      data:
        paged: self.paged
        perpage: self.perpage
    .then (results)->
      for item in results
        item.coupon = app.parse_coupon(item.coupon)
      self.setData
        coupons: self.data.coupons.concat(results)
        has_more: results.length >= self.perpage and self.paged < 60
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
