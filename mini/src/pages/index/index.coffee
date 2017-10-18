core = require('../../core.js')
restStore = require('../../restapi/store.js')

app = getApp()

Page
  data:
    image: core.image
    coupons: []
    promotions: []
    categories: []
    ad: null


  # lifecycle
  onLoad: (opts)->
    self = @
    # app.goto
    #   route: '/pages/post/detail'
    #   query:
    #     # link_id: "59da4fca1697968a1671696e"
    #     org: "test"
    #     # post_id: "59d809c81697961852d30a5d"
    #     post_id: "59d966151697965935aee113"
    self.list()

  onShareAppMessage: ->
    share_opts =
      imageUrl: core.config.splash
    return share_opts

  onPullDownRefresh: ->
    self = @
    self.list()
    .finally ->
      wx.stopPullDownRefresh()


  # hanlders
  list: ->
    self = @
    restStore.coupon.list()
    .then (results)->
      for item in results
        item.coupon = app.parse_coupon(item.coupon)
      self.setData
        coupons: self.data.coupons.concat(results)

  enter: (e)->
    item = e.currentTarget.dataset.item
    return if not item
    app.current_item.set(item)
    app.goto
      route: '/pages/index/item'
