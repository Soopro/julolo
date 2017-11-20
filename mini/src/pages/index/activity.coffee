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
    activity: null

  paged: 1
  perpage: 12
  timestamp: utils.now()

  # lifecycle
  onShareAppMessage: ->
    self = @
    app.share(self.data.activity)

  onLoad: (opts)->
    self = @
    restStore.activity.get opts.slug
    .then (activity)->
      self.setData
        activity: activity
    .then ->
      self.list_items()

  onPullDownRefresh: ->
    self = @
    self.paged = 1
    self.timestamp = utils.now()
    self.setData
      commodities: []
      has_more: null
    self.list_cat()
    .finally ->
      wx.stopPullDownRefresh()

  onReachBottom: ->
    self = @
    if self.data.has_more is true
      self.paged += 1
      self.list_items()


  # hanlders
  list_items: ->
    self = @
    self.setData
      is_loading: true
    activity_slug = self.data.activity.slug
    restStore.activity.items activity_slug,
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
    app.enter_item(e.currentTarget.dataset.item)

