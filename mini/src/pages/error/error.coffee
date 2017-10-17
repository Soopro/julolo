app = getApp()

Page
  data:
    status: null

  # lifecycle
  onLoad: (opts)->
    self = @

  onPullDownRefresh: ->
    wx.stopPullDownRefresh()

  # hendler
  back: ->
    app.re_launch()