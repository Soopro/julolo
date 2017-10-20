core = require('../../core.js')
utils = require('../../utils.js')
restStore = require('../../restapi/store.js')

app = getApp()

Page
  data:
    profile: null
    items: null
    image: core.image
    show_tip: false

  submitted: false

  # lifecycle
  onLoad: (opts)->
    self = @
    app.get_profile (profile)->
      self.setData
        profile: profile
        show_tip: not wx.getStorageSync('skip_cart_tip')

  onShow: ->
    self = @
    app.cart.refresh()
    self.setData
      items: app.cart.list()

  onPullDownRefresh: ->
    self = @
    if not self.data.items.length and not self.data.show_tip
      self.setData
        show_tip: true
      wx.removeStorageSync('skip_cart_tip')
    wx.stopPullDownRefresh()

  # hanlders
  sync_profile: ->
    self = @
    app.sync_profile (profile)->
      self.setData
        profile: profile

  skip_cart_tip: ->
    self = @
    wx.setStorageSync('skip_cart_tip', true)
    self.setData
      show_tip: false

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
    msg = e.currentTarget.dataset.msg or ''
    return if not item or not item.url or self.submitted
    if item.coupon_code
      self._show_code
        code: item.coupon_code
        content: msg
    else
      self.submitted = true
      restStore.coupon.code
        data:
          text: item.title
          url: item.url
          logo: item.src
      .then (code)->
        item.coupon_code = code.code
        app.cart.update(item)
        self.setData
          items: app.cart.list()
        self._show_code
          code: item.coupon_code
          content: msg
      .finally ->
        self.submitted = false

  _show_code: (opts)->
    wx.setClipboardData
      data: opts.code
    core.dialog.alert
      title: opts.code
      content: opts.content
