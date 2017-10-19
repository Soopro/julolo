core = require('../../core.js')
utils = require('../../utils.js')
restStore = require('../../restapi/store.js')

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
    app.cart.refresh()
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
    toast_title = e.currentTarget.dataset.title or ''
    return if not item
    restStore.coupon.code
      data:
        text: item.title
        url: item.coupon_url
    .then (code)->
      console.log code
      item.coupon_code = code.code
      app.cart.update(item)

      wx.setClipboardData
        data: code.code

      wx.showToast
        title: toast_title
        icon: 'success'
        mask: true
        duration: 3000

