core = require('../core.js')

request = (opts)->
  if not opts
    opts = {}

  promise = new Promise (resolve, reject)->
    if opts.navbar_loading
      wx.showNavigationBarLoading()

    if typeof(core.interceptor) is 'function'
      opts = core.interceptor(opts)

    opts.success = (res) ->
      if res.statusCode >= 400
        if typeof(opts.before_reject) is 'function'
          opts.before_reject(res)
        reject(res)
      else
        resolve(res.data, res)

    opts.fail = (res) ->
      reject(res)

    opts.complete = ->
      if opts.navbar_loading
        wx.hideNavigationBarLoading()

    wx.request(opts)

  return promise


request_get = (path, opts)->
  opts = {} if not opts
  opts.path = path
  opts.method = 'GET'
  request(opts)


request_put = (path, opts)->
  opts = {} if not opts
  opts.path = path
  opts.method = 'PUT'
  request(opts)


request_post = (path, opts)->
  opts = {} if not opts
  opts.path = path
  opts.method = 'POST'
  request(opts)


request_del = (path, opts)->
  opts = {} if not opts
  opts.path = path
  opts.method = 'DELETE'
  request(opts)


module.exports =
  request: request
  get: request_get
  put: request_put
  update: request_put
  post: request_post
  del: request_del
  remove: request_del
