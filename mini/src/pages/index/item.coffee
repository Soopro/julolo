core = require('../../core.js')
app = getApp()

Page
  data:
    image: core.image
    item: null

  # lifecycle
  onShareAppMessage: app.share

  onShow: ->
    self = @
    item = app.g.current_item
    console.log item
    if not item
      app.re_launch()
    else
      self.setData
        item: item

  onPullDownRefresh: ->
    wx.stopPullDownRefresh()


  # hanlders
  add_to_cart: (e)->
    console.log 'add to cart'
