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
    promotions: []
    cat_groups: []
    shortcuts: []
    banners: []

  paged: 1
  perpage: 12
  limit: 60
  timestamp: utils.now()

  # lifecycle
  onShareAppMessage: app.share

  onLoad: (opts)->
    self = @
    self.refresh()


  onPullDownRefresh: ->
    self = @
    self.refresh()
    .finally ->
      wx.stopPullDownRefresh()

  onReachBottom: ->
    self = @
    if self.data.has_more is true
      self.paged += 1
      self.list()


  # hanlders
  refresh: ->
    self = @
    self.paged = 1
    self.timestamp = utils.now()
    self.setData
      commodities: []
      has_more: null
    restStore.promotion.list()
    .then (promotions)->
      self.setData
        promotions: promotions
    .then ->
      restStore.category.list()
    .then (categories)->
      self.setData
        cat_groups: self._group_categories(categories)
    .then ->
      restStore.shortcut.list()
    .then (shortcuts)->
      self.setData
        shortcuts: shortcuts
    .then ->
      self.list()

  list: ->
    self = @
    self.setData
      is_loading: true
    restStore.commodity.list
      data:
        paged: self.paged
        perpage: self.perpage
        timestamp: self.timestamp
        newest: true
    .then (results)->
      for item in results
        item.coupon = app.parse_coupon(item.coupon_info)
      self.setData
        commodities: self.data.commodities.concat(results)
        has_more: results[0] and results[0]._more and self.paged < self.limit
    .finally ->
      self.setData
        is_loading: false

  enter_promo: (e)->
    promo = e.currentTarget.dataset.promo
    app.goto
      route: '/pages/index/promotion'
      query:
        slug: promo.slug

  enter_category: (e)->
    cat = e.currentTarget.dataset.category
    app.goto
      route: '/pages/index/category'
      query:
        slug: cat.slug

  enter_shortcut: (e)->
    shortcut = e.currentTarget.dataset.shortcut
    path_pairs = shortcut.path.split('?')
    route = path_pairs[0]
    params = (path_pairs[1] or '').split('&') or []
    query_obj = {}
    for param in params
      key_pairs = param.split('=')
      continue if not key_pairs[0] or not key_pairs[1]
      query_obj[key_pairs[0]] = key_pairs[1]

    app.goto
      route: '/pages/' + route
      query: query_obj

  enter: (e)->
    app.enter_item(e.currentTarget.dataset.item)

  # helpers
  _group_categories: (categories)->
    limit = core.config.category_group_limit or 8
    group = []
    results = []
    for cat in categories
      group.push(cat)
      if group.length >= limit
        results.push(group)
        group = []
    if group.length
      results.push(group)
    return results
