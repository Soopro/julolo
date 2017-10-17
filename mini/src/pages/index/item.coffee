core = require('../../core.js')
restGoods = require('../../restapi/goods.js')

app = getApp()

Page
  data:
    image: core.image
    orgs: []


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
    restOrg.list()
    .then (orgs)->
      self.setData
        orgs: orgs

  enter: (e)->
    org = e.currentTarget.dataset.org
    app.goto
      route: '/pages/org/org'
      query:
        org: org.slug
