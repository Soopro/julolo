config = require('config.js')
utils = require('utils.js')
image = require('constant/image.js')


# promise
Promise.prototype['finally'] = (callback) ->
  constructor = @constructor
  @then ((value) ->
    constructor.resolve(callback()).then ->
      value
  ), (reason) ->
    constructor.resolve(callback()).then ->
      throw reason
      return


# interceptor
interceptor = (opts)->
  if not opts.url
    opts.url = config.baseURL.api + (opts.path or '')

  opts.before_reject = (res)->
    switch res.statusCode
      when 401
        to_url = config.paths.login
        wx.removeStorageSync('auth')
      when 403
        to_url = config.paths.banned
        wx.removeStorageSync('auth')
      else
        to_url = config.paths.error
    if to_url
      wx.redirectTo
        url: to_url

  opts.header = opts.header or {}
  auth = wx.getStorageSync('auth') or {}
  token = auth.token
  if token and not opts.header.Authorization
    opts.header =
      Authorization: "Bearer #{token}"

  return opts


# authorize before run
authorize_run = (opts, callback, fail_callback)->
  opts = {} if not opts
  if not utils.isFunction(callback)
    callback = ->
  if not utils.isFunction(fail_callback)
    fail_callback = ->

  wx.getSetting
    success: (data) ->
      if data.authSetting[opts.scope]
        callback(data)
      else if opts.required
        if data.authSetting[opts.scope] is undefined
          callback(data)
        else if data.authSetting[opts.scope] is false
          wx.openSetting
            success: (op_data)->
              if op_data.authSetting[opts.scope]
                callback(data)
            fail: (error)->
              fail_callback(error)
    fail: (error)->
      fail_callback(error)


# make userinfo to profile
make_profile = (userinfo) ->
  profile =
    country: userinfo.country or ''
    province: userinfo.province or ''
    city: userinfo.city or ''
    language: userinfo.language or 'zh_CN'
    name: userinfo.nickName or ''
    avatar: userinfo.avatarUrl or ''
    gender: userinfo.gender or 0
  return profile


# form validator
_validator =
  required: (value)->
    return /.+/i.test(value.replace(' ', ''))

_validation = (rules, value)->
  if utils.isString(rules)
    rules = [rules]
  else if not utils.isArray(rules)
    return null
  for rule in rules
    try
      if _validator[rule] and not _validator[rule](value)
         return false
    catch
      return false
  return true

form_validator =
  validate: (from_value, rules)->
    return if not utils.isDict(rules, true)
    ffv = {}
    for k, v of from_value
      ffv[k] = _validation(rules[k], v)
    for k, v of ffv
      ffv.$error = true if v is false
    return ffv

  setPristine: (ffv, field_name)->
    try
      delete ffv[field_name]
    catch e
      console.error e
    for k, v of ffv
      ffv.$error = true if v is false
    return ffv


# model
dialog =
  confirm: (opts)->
    opts = {} if not opts
    if not utils.isFunction(opts.confirm)
      opts.confirm = ->
    if not utils.isFunction(opts.cancel)
      opts.cancel = ->

    modal_opts =
      title: opts.title or ''
      content: opts.content or ''
      success: (result)->
        if result.confirm
          opts.confirm()
        else
          opts.cancel(result.cancel)
      fail: ->
        opts.cancel(null)

    if opts.confirmColor
      modal_opts.confirmColor = opts.confirmColor
    if opts.confirmText
      modal_opts.confirmText = opts.confirmText
    if opts.cancelColor
      modal_opts.cancelColor = opts.cancelColor
    if opts.cancelText
      modal_opts.cancelText = opts.cancelText

    wx.showModal(modal_opts)

  alert: (opts)->
    opts = {} if not opts
    if not utils.isFunction(opts.confirm)
      opts.confirm = ->
    modal_opts =
      title: opts.title or '',
      content: opts.content or '',
      showCancel: false
      success: (result)->
        if result.confirm
          opts.confirm()
    if opts.confirmColor
      modal_opts.confirmColor = opts.confirmColor
    if opts.confirmText
      modal_opts.confirmText = opts.confirmText

    wx.showModal(modal_opts)


# Stack
class Stack
  constructor: (fields)->
    self = @
    self.stack = {}
    for field in fields
      self.stack[field] = []

  fieldError: ->
    throw new Error('Stack: field does not exist.')

  get: (field)->
    self = @
    self.fieldError() if not field of self.stack
    return self.stack[field]

  len: (field)->
    self = @
    self.fieldError() if not field of self.stack
    return self.stack[field].length

  push: (item, field)->
    self = @
    if field
      if field of self.stack
        self.stack[field].push item
      else
        self.fieldError()
    else
      for field, _ of self.stack
        self.stack[field].push item

  popup: (field) ->
    self = @
    self.fieldError() if not field of self.stack
    return self.stack[field].pop()

  clean: (field)->
    self = @
    if field
      if field of self.stack
        self.stack[field].length = 0
      else
        self.fieldError()
    else
      for field, _ of self.stack
        self.stack[field].length = 0


# Cart
class Cart
  constructor: (key, list, limit, expires_in)->
    self = @
    self.cart_key = key or '_cart_storage'
    self.cart_limit = limit or 600
    self.expires_in = 3600 * 24 * 7
    self.load(list) if utils.isArray(list, true)

  _limit: (list)->
    self = @
    if list.length > self.cart_limit
      list.length = self.cart_limit

  load: (list)->
    self = @
    self._limit(list)
    wx.setStorageSync(self.cart_key, list)

  refresh: ->
    self = @
    _now = utils.now()
    cart_list = self.list()
    cart_list = (item for item in cart_list \
      when (_now - item._added) < self.expires_in)
    wx.setStorageSync(self.cart_key, cart_list)

  list: ->
    self = @
    cart_list = wx.getStorageSync(self.cart_key) or []
    self._limit(cart_list)
    return cart_list

  len: ->
    self = @
    cart_list = self.list()
    return cart_list.length

  get: (item_id)->
    self = @
    return null if not item_id
    cart_list = self.list()
    return utils.list.get(cart_list, {'id': item_id}, 'id')

  add: (item)->
    self = @
    return if not item
    item._added = utils.now()
    cart_list = self.list()
    utils.list.remove(cart_list, item, 'id')
    cart_list.unshift(item)
    self._limit(cart_list)
    wx.setStorageSync(self.cart_key, cart_list)

  remove: (item_id) ->
    self = @
    return if not item_id
    cart_list = self.list()
    utils.list.remove(cart_list, {'id': item_id}, 'id')
    wx.setStorageSync(self.cart_key, cart_list)

  update: (item)->
    self = @
    _now = utils.now()
    cart_list = self.list()
    idx = utils.list.index(cart_list, item, 'id')
    if idx
      cart_list[idx] = item
    else
      cart_list.unshift(item)
    wx.setStorageSync(self.cart_key, cart_list)

  clean: ->
    self = @
    wx.setStorageSync(self.cart_key, [])


module.exports =
  config: config
  image: image
  interceptor: interceptor
  make_profile: make_profile
  authorize_run: authorize_run
  form_validator: form_validator
  dialog: dialog
  Stack: Stack
  Cart: Cart
