core = require('core.js')
utils = require('utils.js')

# Decorators

login_required = (fn)->
  if not utils.isFunction(fn)
    fn = ->

  wrapped_fn = (opts)->
    self = @
    if wx.getStorageSync('auth')
      return fn.call(self, opts)
    else
      if utils.isObject(opts.target, true)
        opts = null
      warp_point =
        route: self.route or ''
        query: opts or {}
      wx.setStorageSync('warp_point', warp_point)
      wx.redirectTo
        url: core.config.paths.login

  return wrapped_fn

module.exports = {}
