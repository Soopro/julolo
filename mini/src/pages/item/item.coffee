core = require('../../core.js')
restStore = require('../../restapi/store.js')


app = getApp()

Page
  data:
    image: core.image
    item: null
    details: []

  id: null
  submitted: false

  # lifecycle
  onShareAppMessage: ->
    self = @
    app.share(self.data.item)

  onLoad: (opts)->
    self = @
    self.id = opts.id
    item = app.g.current_item
    if item
      self.load_details(item)
      self.setData
        item: item
    else
      self.load_item()


  onPullDownRefresh: ->
    wx.stopPullDownRefresh()


  # hanlders
  load_item: ->
    self = @
    restStore.commodity.get self.id
    .then (item)->
      self.load_details(item)
      self.setData
        item: item

  load_details: (item)->
    self = @
    restStore.details.get item.item_id
    .then (details)->
      self.setData
        details: details

  buy: ->
    self = @
    item = self.data.item
    return if not item or not item.url or self.submitted

    buy_item = app.cart.get(item.id)
    if buy_item
      app.show_coupon
        code: buy_item.coupon_code
        msg: buy_item.coupon_msg
    else
      self.submitted = true
      restStore.coupon.code
        data:
          text: item.title
          url: item.url
          logo: item.src
          item: item
      .then (code)->
        if code.code
          app.cart.add
            id: item.id
            price: item.price
            src: item.src
            title: item.title
            url: item.url
            coupon_info: item.coupon_info
            coupon_code: code.code
            coupon_msg: code.msg
        app.show_coupon
          code: code.code
          msg: code.msg
      .catch (error)->
        console.log error
      .finally ->
        self.submitted = false

  try_to_buy: (e)->
    self = @
    data = e.currentTarget.dataset
    return if not data
    core.dialog.confirm
      title: data.title
      content: data.content
      confirmText: data.confirmText
      cancelText: data.cancelText
      confirm: ->
        self.buy()
