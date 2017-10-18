core = require('../../core.js')
restStore = require('../../restapi/store.js')

app = getApp()

Page
  data:
    image: core.image
    coupons: []


  # lifecycle
  onLoad: (opts)->
    self = @

  onShareAppMessage: ->
    share_opts =
      imageUrl: '/img/splash.jpg'
    return share_opts

  onPullDownRefresh: ->
    self = @
    self.setData
      coupons: []
    wx.stopPullDownRefresh()


  # hanlders
  search: ->
    self = @
    restStore.search()
    .then (results)->
      self.setData
        coupons: results

  enter: (e)->
    item = e.currentTarget.dataset.item
    return if not item
    app.current_item.set(item)
    app.goto
      route: '/pages/index/item'
