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
    category: null

  paged: 1
  perpage: 12
  last_paged: 1
  timestamp: utils.now()
  remote_query: false

  # lifecycle
  onShareAppMessage: ->
    self = @
    app.share(self.data.category)

  onLoad: (opts)->
    self = @
    restStore.category.get opts.slug
    .then (category)->
      self.setData
        category: category
    .then ->
      self.list_cat()

  onPullDownRefresh: ->
    self = @
    self.paged = 1
    self.last_paged = 1
    self.timestamp = utils.now()
    self.remote_query = false
    self.setData
      commodities: []
      has_more: null
    self.list_cat()
    .finally ->
      wx.stopPullDownRefresh()

  onReachBottom: ->
    self = @
    if self.data.has_more is true
      self.load_more()

  # hanlders
  list_cat: ->
    self = @
    self._query_items()

  load_more: ->
    self = @
    self.paged += 1
    if not self.remote_query
      self._query_items()
    else
      self._query_remote()

  enter: (e)->
    app.enter_item(e.currentTarget.dataset.item)


  # helpers
  _query_items: ->
    self = @
    self.setData
      is_loading: true
    restStore.commodity.list
      data:
        categories: self.data.category.cat_ids
        paged: self.paged
        perpage: self.perpage
        timestamp: self.timestamp
    .then (results)->
      for item in results
        item.coupon = app.parse_coupon(item.coupon_info)
      if not results.length or not results[0]._more
        self.remote_query = true
        self.last_paged = self.paged
      if results.length
        self.setData
          has_more: true
          commodities: self.data.commodities.concat(results)
      if self.paged == 1 and self.remote_query
        self.load_more()
    .finally ->
      self.setData
        is_loading: false

  _query_remote: ->
    self = @
    self.setData
      is_loading: true
    restStore.coupon.list
      data:
        categories: self.data.category.cat_ids
        paged: self.paged - self.last_paged
        perpage: self.perpage
    .then (results)->
      for item in results
        item.coupon = app.parse_coupon(item.coupon_info)
      self.setData
        commodities: self.data.commodities.concat(results)
        has_more: results.length >= self.perpage
    .finally ->
      self.setData
        is_loading: false
