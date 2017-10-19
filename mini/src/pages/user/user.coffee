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

  help: ->
    app.goto
      route: core.config.paths.help
      method: wx.switchTab

  gobuy: ->
    app.goto
      route: core.config.paths.index
      method: wx.switchTab

  clean: ->
    self = @
    app.cart.clean()
    self.setData
      items: []

  use: (e)->
    self = @
    item = e.currentTarget.dataset.item
    return if not item
    app.cart.use(item)
