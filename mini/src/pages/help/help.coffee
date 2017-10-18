core = require('../../core.js')
utils = require('../../utils.js')
restStore = require('../../restapi/store.js')

app = getApp()

Page
  data:
    help: null
    image: core.image

  # lifecycle
  onLoad: (opts)->
    self = @
    self.get_help()

  onPullDownRefresh: ->
    self = @
    self.get_help()
    .finally ->
      wx.stopPullDownRefresh()

  # hanlders
  get_help: ->
    self = @
    restStore.info()
    .then (store_info)->
      self.setData
        help: store_info.help_src


  debug: app.debug
