core = require('../../core.js')
restGoods = require('../../restapi/goods.js')

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

    # wx.switchTab
    #   url: '/pages/user/user'
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
    restGoods.coupon.list()
    .then (coupons)->
      self.setData
        coupons: coupons

  enter: (e)->
    org = e.currentTarget.dataset.org
    app.goto
      route: '/pages/org/org'
      query:
        org: org.slug
