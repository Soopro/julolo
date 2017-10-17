requests = require('requests.js')

report_post = (org_slug, post_id, opts) ->
  requests.post('/report/'+org_slug+'/'+post_id, opts)


module.exports =
  report_post: report_post
