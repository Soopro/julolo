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

  onPullDownRefresh: ->
    wx.stopPullDownRefresh()


  # hanlders
  buy: (e)->
    self = @
    toast_title = e.currentTarget.dataset.title or ''
    item = self.data.item
    app.cart.add
      id: item.id
      price: item.price
      src: item.src
      title: item.title
      url: item.url
      coupon: item.coupon

    wx.showToast
      title: toast_title
      icon: 'success'
      mask: true
