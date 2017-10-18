utils = require('../../utils.js')
restStore = require('../../restapi/store.js')

app = getApp()

Page
  data:
    tips: []

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
    restStore.tip.list()
    .then (tips)->
      self.setData
        tips: tips

  debug: app.debug
