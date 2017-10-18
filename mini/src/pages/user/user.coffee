core = require('../../core.js')
utils = require('../../utils.js')

app = getApp()

Page
  data:
    profile: null
    items: []
    image: core.image

  # lifecycle
  onLoad: (opts)->
    self = @
    app.get_profile (profile)->
      self.setData
        profile: profile

  onShow: ->
    self = @
    self.setData
      items: app.cart.list()

  onPullDownRefresh: ->
    wx.stopPullDownRefresh()

  # hanlders
  sync_profile: ->
    self = @
    app.sync_profile (profile)->
      console.log profile
      self.setData
        profile: profile

  remove: (e)->
    self = @
    item = e.currentTarget.dataset.item
    return if not item
    app.cart.remove(item)
    utils.list.remove(self.data.items, item, 'id')
    self.setData
      items: self.data.items

  clear: ->
    self = @
    app.cart.clear(item)
    self.setData
      items: []

  use: (e)->
    self = @
    item = e.currentTarget.dataset.item
    return if not item
    app.cart.use(item)
