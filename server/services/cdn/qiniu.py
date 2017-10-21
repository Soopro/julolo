# coding=utf-8
from __future__ import absolute_import

import hmac
import hashlib
import base64
import time
import json
import requests
import urllib
from urlparse import urlparse


class Qiniu(object):
    API_URL = {
        'http': {
            'RS': 'http://rs.qiniu.com',
            'RSF': 'http://rsf.qiniu.com',
            'UP': 'http://up.qiniu.com'
        },
        'https': {
            'RS': 'https://rs.qbox.me',
            'RSF': 'https://rsf.qbox.me',
            'UP': 'https://up.qbox.me'
        }
    }
    # up.qiniu seems is directly upload to thier server.
    # upload.qiniu will upload to cdn, then to thier server.

    DEPRECATED_POLICY_FIELDS = set([
        'asyncOps'
    ])
    POLICY_FIELDS = set([
        'callbackUrl',
        'callbackBody',
        'callbackHost',
        'callbackBodyType',
        'callbackFetchKey',

        'returnUrl',
        'returnBody',

        'endUser',
        'saveKey',
        'insertOnly',

        'detectMime',
        'mimeLimit',
        'fsizeLimit',
        'fsizeMin',

        'persistentOps',
        'persistentNotifyUrl',
        'persistentPipeline',
    ])
    protocol = 'https'
    access_key = None
    secret_key = None
    file_size_limit = 60 * 1024 * 1024
    quality = 90
    timeout = 30

    STYLE_EXTS = ('jpg', 'jpeg', 'png', 'gif')
    ENGINE = '?imageMogr2'

    @staticmethod
    def style_crop(width, height, cx, cy):
        return '/crop/!{0}x{1}a{2}a{3}'.format(width, height, cx, cy)

    @staticmethod
    def style_resize(width, height):
        return '/thumbnail/{0}x{1}!'.format(width, height)

    @staticmethod
    def style_quality(quality):
        return '/quality/{0}'.format(quality)

    def __init__(self, access_key, secret_key, ssl=True,
                 quality=90, file_size_limit=60 * 1024 * 1024,
                 conn_pool=100, max_pool=100, retries=2, timeout=30):
        self.access_key = access_key
        self.secret_key = secret_key
        self.file_size_limit = file_size_limit
        self.quality = quality
        self.timeout = timeout

        self.protocol = 'https' if ssl else 'http'
        self.RS_API = self.API_URL[self.protocol]['RS']
        self.RSF_API = self.API_URL[self.protocol]['RSF']
        self.UPLOAD_API = self.API_URL[self.protocol]['UP']

        # request auth
        self.manager_auth = ManagerAuth(access_key, secret_key)

        # request session
        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(pool_connections=conn_pool,
                                                pool_maxsize=max_pool,
                                                max_retries=retries)
        session.mount('{}://'.format(self.protocol), adapter)
        self._requests = session

    def _copy_policy(self, policy, to, strict_policy):
        for k, v in policy.items():
            if k in self.DEPRECATED_POLICY_FIELDS:
                continue
            if not strict_policy or k in self.POLICY_FIELDS:
                to[k] = v

    def _authorize(self, bucket, key=None, expires=3600,
                   policy=None, strict_policy=True):
        scope = bucket
        if key is not None:
            scope = '{}:{}'.format(bucket, key)

        args = {
            'scope': scope,
            'deadline': int(time.time()) + expires,
            'fsizeLimit': self.file_size_limit,
            'returnBody': json.dumps({
                'name': '$(fname)',
                'mimetype': '$(mimeType)',
                'ext': '$(ext)',
                'size': '$(fsize)',
                'w': '$(imageInfo.width)',
                'h': '$(imageInfo.height)',
                'hash': '$(etag)',
                'key': '$(key)'
            })
        }

        if policy is not None:
            self._copy_policy(policy, args, strict_policy)

        # data
        data = json.dumps(args, separators=(',', ':'))
        data = base64.urlsafe_b64encode(data)

        # private_token
        sha1 = hmac.new(self.secret_key, data, hashlib.sha1)
        private_token = base64.urlsafe_b64encode(sha1.digest())

        return '{0}:{1}:{2}'.format(self.access_key, private_token, data)

    def _list(self, bucket, prefix):
        # list
        params = {
            'bucket': bucket,
            'prefix': prefix,
            'limit': 1000,
            # 'marker': ''  # the start point
        }
        params_encoded = urllib.urlencode(params)
        list_url = '{}/{}?{}'.format(self.RSF_API, 'list', params_encoded)
        r = self._requests.post(list_url,
                                auth=self.manager_auth,
                                timeout=self.timeout)
        r.raise_for_status()
        """
        Properties:
        marker  -- str the mark point for next list, empty str if no more.
        items   -- list result entires.
        ...
        """
        return r.json()

    def _delete(self, bucket, key):
        res = base64.urlsafe_b64encode('{0}:{1}'.format(bucket, key))
        cmd = '{}/{}'.format('delete', res)
        url = '{}/{}'.format(self.RS_API, cmd)

        r = self._requests.post(url, auth=self.manager_auth)
        r.raise_for_status()
        return

    def _batch_delete(self, bucket, keys):
        operations = []
        for key in keys:
            res = base64.urlsafe_b64encode('{0}:{1}'.format(bucket, key))
            cmd = '/{}/{}'.format('delete', res)
            operations.append(cmd)

        batch_url = '{}/{}'.format(self.RS_API, 'batch')

        r = self._requests.post(batch_url,
                                data={'op': operations},
                                auth=self.manager_auth,
                                timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def authorize(self, bucket, key=None, expires=3600,
                  policy=None, strict_policy=True):
        return self._authorize(bucket, key, expires, policy, strict_policy)

    def delete(self, bucket, key):
        return self._delete(bucket, key)

    def batch_delete(self, bucket, keys):
        return self._batch_delete(bucket, keys)

    def upload(self, bucket, key, c_file, mimetype=None, headers=None):
        if mimetype is None:
            mimetype = 'application/octet-stream'
        url = self.UPLOAD_API
        fields = {
            'key': key,
            'token': self._authorize(bucket, key)
        }
        files = {'file': (c_file['filename'], c_file['stream'], mimetype)}
        r = self._requests.post(url, headers=headers, files=files,
                                data=fields, timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def info(self, bucket, key):
        res = base64.urlsafe_b64encode('{0}:{1}'.format(bucket, key))
        cmd = '{}/{}'.format('stat', res)
        url = '{}/{}'.format(self.RS_API, cmd)
        r = self._requests.post(url,
                                auth=self.manager_auth,
                                timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def clear(self, bucket, prefix, recursive=True):
        result = self._list(bucket, prefix)
        try:
            keys = [item.get('key') for item in result.get('items', [])]
        except Exception:
            raise Exception('clear: bad result')

        if not keys:
            return True

        self._batch_delete(bucket, keys)

        if recursive:
            self.clear(bucket=bucket, prefix=prefix)
        return False


# auth class
class ManagerAuth(requests.auth.AuthBase):
    FROM_CONTENT_TYPE = 'application/x-www-form-urlencoded'
    access_key = None
    secret_key = None

    def __init__(self, access_key, secret_key):
        self.access_key = access_key
        self.secret_key = secret_key

    def __call__(self, r):
        token = None
        if r.body is not None \
                and r.headers['Content-Type'] == self.FROM_CONTENT_TYPE:
            token = self._authorize(r.url, r.body)
        else:
            token = self._authorize(r.url)
        r.headers['Authorization'] = 'QBox {0}'.format(token)
        return r

    def _authorize(self, url, body=None, content_type=None):
        parsed_url = urlparse(url)
        query = parsed_url.query
        path = parsed_url.path
        data = path
        if query != '':
            data = ''.join([data, '?', query])
        data = ''.join([data, '\n'])

        if body:
            data += body

        sha1 = hmac.new(self.secret_key, data, hashlib.sha1)
        private_token = base64.urlsafe_b64encode(sha1.digest())

        return '{0}:{1}'.format(self.access_key, private_token)
