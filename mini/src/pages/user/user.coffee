core = require('../../core.js')
deco = require('../../decorators.js')
utils = require('../../utils.js')
restUser = require('../../restapi/user.js')

app = getApp()

Page
  data:
    profile: null
    posts: []
    has_more: null
    is_loading: null
    image: core.image

  # internal
  showtime: 0

  # lifecycle
  onLoad: (opts)->
    self = @
    app.get_profile (profile)->
      self.setData
        profile: profile
      self.load_prop_posts(true)

  onShow: ->
    self = @
    posts = self.data.posts
    removed_count = app.removedStack.len('PROP_POSTS')
    if removed_count and posts.length > 0
      for rm in app.removedStack.get('PROP_POSTS')
        utils.list.remove(posts, rm, 'id')
      app.removedStack.clean('PROP_POSTS')
      self.setData
        posts: posts

  onPullDownRefresh: ->
    self = @
    if self._allow_load_prop_posts(true)
      self.load_prop_posts(true)
      .finally ->
        wx.stopPullDownRefresh()

  onReachBottom: ->
    self = @
    if self._allow_load_prop_posts()
      self.load_prop_posts()

  # hanlders
  sync_profile: ->
    self = @
    app.sync_profile (profile)->
      if not self.data.profile
        self.load_prop_posts(true)

      self.setData
        profile: profile


  read: (e)->
    post = e.currentTarget.dataset.post
    app.goto
      route: '/pages/post/detail'
      query:
        org: post.org_slug
        post_id: post.id

  _allow_load_prop_posts: (refresh)->
    self = @
    is_loading = self.data.is_loading
    more = (self.data.has_more isnt false) or refresh
    return more and not is_loading

  load_prop_posts: (refresh)->
    self = @

    if refresh
      self.query_timestamp = null
      self.setData
        has_more: null

    posts = if refresh then [] else self.data.posts

    console.log 'Load prop posts:', posts.length

    self.setData
      is_loading: true

    self.query_timestamp = (utils.now() - 1) if not self.query_timestamp
    restUser.prop.list
      data:
        offset: posts.length
        timestamp: self.query_timestamp
    .then (results)->
      _last = results[0] or {_more: false}  # for empty list.
      self.setData
        has_more: _last._more
        posts: posts.concat(results)
    .finally ->
      self.setData
        is_loading: false

  debug: app.debug
