core = require('../../core.js')
restStore = require('../../restapi/store.js')

app = getApp()

Page
  data:
    image: core.image
    search_key: null
    coupons: []

  paged: 1
  perpage: 60

  # lifecycle
  onLoad: (opts)->
    self = @

  onPullDownRefresh: ->
    self = @
    self.paged = 1
    self.setData
      coupons: []
    wx.stopPullDownRefresh()


  # hanlders
  search: (e)->
    self = @
    if e.type is 'submit'
      keyword = e.detail.value.keyword
    else if e.type is 'confirm'
      keyword = e.detail.value
    else
      keyword = null

    return if not keyword

    restStore.coupon.search
      data:
        paged: self.paged
        perpage: self.perpage
        keyword: keyword
    .then (results)->
      for item in results
        item.coupon = app.parse_coupon(item.coupon)
      self.paged += 1
      self.setData
        coupons: results

  enter: (e)->
    item = e.currentTarget.dataset.item
    return if not item
    app.current_item.set(item)
    app.goto
      route: '/pages/index/item'
