requests = require('requests.js')

login = (opts)->
  requests.post('/wx/mini/login', opts)

get_profile = (opts)->
  requests.get('/user/profile', opts)

update_profile = (opts)->
  requests.update('/user/profile', opts)

list_prop_posts = (opts)->
  requests.get('/user/property/post', opts)


module.exports =
  login: login
  profile:
    get: get_profile
    update: update_profile
  prop:
    list: list_prop_posts
