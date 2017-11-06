core = require('../../core.js')
utils = require('../../utils.js')
restStore = require('../../restapi/store.js')


app = getApp()

Page
  data:
    image: core.image
    search_key: null
    has_more: null
    is_loading: null
    commodities: []

  paged: 1
  perpage: 12
  keyword: null
  last_paged: 1
  timestamp: utils.now()
  remote_search: false


  # lifecycle
  onShareAppMessage: app.share

  onLoad: (opts)->
    self = @

  onPullDownRefresh: ->
    self = @
    self.paged = 1
    self.last_paged = 1
    self.timestamp = utils.now()
    self.remote_search = false
    self.setData
      commodities: []
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
      commodities: []
      has_more: null
    wx.showLoading
      mask: true
    self._search()
    .finally ->
      wx.hideLoading()

  load_more: ->
    self = @
    self.paged += 1
    if not self.remote_search
      self._search()
    else
      self._search_remote()

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
    restStore.commodity.search
      data:
        paged: self.paged
        perpage: self.perpage
        keyword: self.keyword
        timestamp: self.timestamp
    .then (results)->
      for item in results
        item.coupon_info = app.parse_coupon(item.coupon_info)
      if not results.length or not results[0]._more
        self.remote_search = true
        self.last_paged = self.paged
      if results.length
        self.setData
          commodities: self.data.commodities.concat(results)
      else
        self.load_more()
    .finally ->
      self.setData
        is_loading: false

  _search_remote: ->
    self = @
    self.setData
      is_loading: true
    restStore.coupon.search
      data:
        paged: self.paged - self.last_paged
        perpage: self.perpage
        keyword: self.keyword
    .then (results)->
      for item in results
        item.is_remote = true
        item.coupon_info = app.parse_coupon(item.coupon_info)
      self.setData
        commodities: self.data.commodities.concat(results)
        has_more: results.length >= self.perpage
    .finally ->
      self.setData
        is_loading: false
