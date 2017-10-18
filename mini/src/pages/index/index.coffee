core = require('../../core.js')
restStore = require('../../restapi/store.js')

app = getApp()

Page
  data:
    image: core.image
    coupons: []
    promotions: [
      {
        src: 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg'
        label: 'Testgy'
      }
      {
        src: 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg'
        label: 'Test'
      }
      {
        src: 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg'
        label: 'Test'
      }
    ]
    categories: [
      {
        src: 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg'
        label: 'Testgy'
      }
      {
        src: 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg'
        label: 'Test'
      }
      {
        src: 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg'
        label: 'Test'
      }
      {
        src: 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg'
        label: 'Test'
      }
      {
        src: 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg'
        label: 'Test'
      }
      {
        src: 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg'
        label: 'Test'
      }
      {
        src: 'http://img2.sucaifengbao.com/813/813b_109_XVTb.jpg'
        label: 'Test'
      }
    ]
    ad:
      id: '123'
      src: 'http://www.3dmgame.com/uploads/allimg/150608/276_150608083901_1.jpg'



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

    wx.switchTab
      url: '/pages/help/help'
    return
    self.list()

  onShareAppMessage: ->
    share_opts =
      imageUrl: '/img/splash.jpg'
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
        item.coupon = item.coupon.replace(/满.*?元/ig, '')
      self.setData
        coupons: self.data.coupons.concat(results)

  enter: (e)->
    item = e.currentTarget.dataset.item
    return if not item
    app.current_item.set(item)
    app.goto
      route: '/pages/index/item'
