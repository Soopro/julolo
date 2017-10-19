core = require('../../core.js')
restStore = require('../../restapi/store.js')

app = getApp()

Page
  data:
    image: core.image
    search_key: null
    has_more: null
    is_loading: null
    coupons: []

  paged: 1
  perpage: 60
  keyword: null

  # lifecycle
  onShareAppMessage: app.share

  onLoad: (opts)->
    self = @

  onPullDownRefresh: ->
    self = @
    self.paged = 1
    self.setData
      coupons: []
      has_more: null
    wx.stopPullDownRefresh()

  onReachBottom: ->
    self = @
    if self.keyword and self.data.has_more is true
      self.load_more()

  # hanlders
  search: (e)->
    self = @
    if e.type is 'submit'
      keyword = e.detail.value.keyword
    else if e.type is 'confirm'
      keyword = e.detail.value
    else
      keyword = null

    return if not keyword

    self.keyword = keyword
    self.setData
      coupons: []
      has_more: null
    self._search()

  load_more: ->
    self = @
    self.paged += 1
    self._search()

  enter: (e)->
    item = e.currentTarget.dataset.item
    return if not item
    app.g.current_item = item
    app.goto
      route: '/pages/index/item'

  # helpers
  _search: ->
    self = @
    self.setData
      is_loading: true
    restStore.coupon.search
      data:
        paged: self.paged
        perpage: self.perpage
        keyword: self.keyword
    .then (results)->
      for item in results
        item.coupon = app.parse_coupon(item.coupon)
      self.setData
        coupons: self.data.coupons.concat(results)
        has_more: results.length >= self.perpage
    .finally ->
      self.setData
        is_loading: false
