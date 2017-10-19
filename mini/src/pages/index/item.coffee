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
    if not item
      app.re_launch()
    else
      self.setData
        item: item
    console.log app.cart.get()

  onPullDownRefresh: ->
    wx.stopPullDownRefresh()


  # hanlders
  buy: ->
    self = @
    item = self.data.item
    app.cart.add
      id: item.id
      price: item.price
      src: item.src
      title: item.title
      coupon_url: item.coupon_url
      coupon: item.coupon
