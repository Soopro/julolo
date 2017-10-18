app = getApp()

Page
  data:
    item: null


  # lifecycle
  onShow: ->
    self = @
    item = app.current_item.popup()
    console.log item
    self.setData
      item: item

  onShareAppMessage: ->
    share_opts =
      imageUrl: '/img/splash.jpg'
    return share_opts

  onPullDownRefresh: ->
    wx.stopPullDownRefresh()


  # hanlders
  add_to_cart: (e)->
    console.log 'add to cart'
