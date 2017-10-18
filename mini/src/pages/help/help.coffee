utils = require('../../utils.js')
restStore = require('../../restapi/store.js')

app = getApp()

Page
  data:
    tips: null

  # lifecycle
  onLoad: (opts)->
    self = @
    self.get_tips()

  onPullDownRefresh: ->
    self = @
    self.get_tips()
    .finally ->
      wx.stopPullDownRefresh()

  # hanlders
  get_tips: ->
    self = @
    restStore.info()
    .then (store_info)->
      self.setData
        tips: store_info.tips


  debug: app.debug
