# Config
dev_config =
  baseURL:
    api: 'http://192.168.1.181:15800'

config =
  baseURL:
    api: 'https://api.pupuly.com'

  local_tmp:
    portocal: 'wxfile://'
    prefix: 'tmp_'

  splash: '/img/mini_splash.jpg'
  paths:
    index: '/pages/index/index'
    help: '/pages/help/help'
    error: '/pages/error/error'

  tab_paths: [
    '/pages/index/index'
    '/pages/user/user'
  ]

  post_tags: [
    {key: 'job', name: '求职、招聘'}
    {key: 'second-hand', name: '二手转让'}
    {key: 'rent-house', name: '租房子'}
    {key: 'move', name: '搬家、出远门'}
    {key: 'party', name: '聚会'}
    {key: 'advisor', name: '问答'}
  ]

  post_attach_limit: 4

  dev_mode: ->
    self = @
    return if typeof dev_config isnt 'object'
    for k, v of dev_config
      self[k] = v


module.exports = config
