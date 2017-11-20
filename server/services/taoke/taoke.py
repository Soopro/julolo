# coding=utf-8
from __future__ import absolute_import

import hashlib
import time
import re
import json
import requests


class Taoke(object):
    API_BASE = 'gw.api.taobao.com/router/rest'

    CLICK_BASE_URL = 'https://s.click.taobao.com'
    COUPON_RESTORE_API = 'https://uland.taobao.com/cp/coupon'
    COUPON_BASE_URL = 'https://uland.taobao.com/coupon/edetail'

    ITEM_DETAILS_BASE_URL = 'https://hws.m.taobao.com/cache/' + \
        'mtop.wdetail.getItemDescx/4.1/'

    ACTID_PATTERN = re.compile(ur'[?&](?:activityid|activity_id)=(\w+)', re.I)
    PID_PATTERN = re.compile(ur'&pid=(mm[0-9_]+?)&', re.I)

    DETAILS_KEY_PREFIX = 'taoke.item.details:'
    DETAILS_COUNT_KEY_PREFIX = 'taoke.item.details.count:'

    protocol = 'http'

    headers = {
        'Content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Cache-Control': 'no-cache',
        'Connection': 'Keep-Alive',
    }

    app_key = None
    app_secret = None
    adzone_id = None
    platform = 2  # 1: pc, 2: mobile
    pid = None

    timeout = 30
    expires = 3600 * 24 * 7
    details_limit = 6

    def __init__(self, app_key, app_secret, pid,
                 platform=2, ssl=False, timeout=30,
                 rds_read=None, rds_write=None, expires=None):
        self.app_key = app_key
        self.app_secret = app_secret
        self.pid = pid
        self.adzone_id = pid.split('_')[-1]
        self.platform = platform
        self.timeout = timeout

        self.protocol = 'https' if ssl else 'http'
        # SSL might require SSL verify while request.
        self.API_URL = u'{}://{}'.format(self.protocol, self.API_BASE)

        # redis
        self.rds_read = rds_read
        self.rds_write = rds_write or rds_read

        if expires:
            self.expires = int(expires)

    def _sign(self, req_params):
        keys = req_params.keys()
        keys.sort()
        params_str = u''.join('%s%s' % (key, req_params[key]) for key in keys)
        pm_str = u'{secret}{params}{secret}'.format(secret=self.app_secret,
                                                    params=params_str)
        if isinstance(pm_str, unicode):
            pm_str = pm_str.encode('utf-8')
        return hashlib.md5(pm_str).hexdigest().upper()

    def _make_request(self, api_method, data=None):
        req_params = {
            'format': 'json',
            'sign_method': 'md5',
            'v': '2.0',
            'method': api_method,
            'timestamp': str(long(time.time() * 1000)),
            'app_key': self.app_key,
        }
        sign_params = req_params.copy()
        if data:
            sign_params.update(data)
        req_params['sign'] = self._sign(sign_params)
        r = requests.post(self.API_URL, params=req_params, data=data,
                          headers=self.headers, timeout=self.timeout)
        r.raise_for_status()
        result = r.json()
        if result.get('error_response'):
            raise Exception(result['error_response'])
        return result

    def _list2str(self, iters):
        _list = []
        if isinstance(iters, basestring):
            return iters.replace(' ', '').strip()
        for item in iters:
            try:
                _list.append(str(item).strip())
            except Exception:
                pass
        return ','.join(_list)

    # category
    def list_categories(self, parent_cid=0):
        """
        category api is BASE API, not free.
        """
        api_method = 'taobao.itemcats.get'
        fields = [
            'cid',
            'parent_cid',
            'name',
            'is_parent',
        ]
        data = {
            'parent_cid': parent_cid,
            'fields': ','.join(fields),
        }
        return self._make_request(api_method, data=data)

    # events
    def list_events(self, paged=1, perpage=12):
        """
        events api can get own events only.
        """
        api_method = 'taobao.tbk.uatm.event.get'
        fields = [
            'event_id',
            'event_title',
            'start_time',
            'end_time',
        ]
        data = {
            'page_no': paged,
            'page_size': perpage,
            'fields': ','.join(fields),
        }
        resp = self._make_request(api_method, data=data)
        results = resp['tbk_uatm_event_get_response'].get('results', {})
        return results.get('tbk_event', [])

    def list_event_items(self, event_id, paged=1, perpage=12):
        api_method = 'taobao.tbk.uatm.event.item.get'
        fields = [
            'num_iid',
            'seller_id',
            'title',
            'pict_url',
            'small_images',
            'reserve_price',
            'zk_final_price',
            'zk_final_price_wap',
            'user_type',
            'provcity',
            'item_url',
            'click_url',
            'category',
            'volume',
            'nick',
            'shop_title',
            'event_start_time',
            'event_end_time',
            'tk_rate',
            'status',
            'type',
        ]
        data = {
            'platform': self.platform,
            'adzone_id': self.adzone_id,
            'event_id': event_id,
            'page_no': paged,
            'page_size': perpage,
            'fields': ','.join(fields),
        }
        resp = self._make_request(api_method, data=data)
        resp = resp['tbk_uatm_favorites_item_get_response']
        results = resp.get('results', {})
        return results.get('uatm_tbk_item ', [])

    # favorites
    def list_favorites(self, paged=1, perpage=12, commn_type=-1):
        api_method = 'taobao.tbk.uatm.favorites.get'
        fields = [
            'favorites_title',
            'favorites_id',
            'type',
        ]
        data = {
            'page_no': paged,
            'page_size': perpage,
            'type': commn_type,
            'fields': ','.join(fields),
        }
        resp = self._make_request(api_method, data=data)
        results = resp['tbk_uatm_favorites_get_response'].get('results', {})
        return results.get('tbk_favorites', [])

    def list_favorite_items(self, favorite_id, paged=1, perpage=12):
        api_method = 'taobao.tbk.uatm.favorites.item.get'
        fields = [
            'num_iid',
            'seller_id',
            'title',
            'pict_url',
            'small_images',
            'reserve_price',
            'zk_final_price',
            'zk_final_price_wap',
            'user_type',
            'provcity',
            'item_url',
            'click_url',
            'category',
            'volume',
            'nick',
            'shop_title',
            'event_start_time',
            'event_end_time',
            'coupon_info',
            'coupon_click_url',
            'coupon_start_time',
            'coupon_end_time',
            'coupon_total_count',
            'coupon_remain_count',
            'tk_rate',
            'status',
            'type',
        ]
        data = {
            'platform': self.platform,
            'adzone_id': self.adzone_id,
            'favorites_id': favorite_id,
            'page_no': paged,
            'page_size': perpage,
            'fields': ','.join(fields),
        }
        resp = self._make_request(api_method, data=data)
        resp = resp['tbk_uatm_favorites_item_get_response']
        results = resp.get('results', {})
        return results.get('uatm_tbk_item', [])

    # coupon
    def list_coupons(self, categories=[], search_key=None,
                     paged=1, perpage=12):
        api_method = 'taobao.tbk.dg.item.coupon.get'
        data = {
            'platform': self.platform,
            'adzone_id': self.adzone_id,
            'page_no': paged,
            'page_size': perpage,
        }
        if categories:
            cat_ids = self._list2str(categories)
            """
            'cat' limit to 10, otherwise 'Invalid arguments:cat, code 41'
            """
            if len(cat_ids) > 10:
                cat_ids = cat_ids.split(',')[0]
            data['cat'] = cat_ids

        if search_key:
            data['q'] = search_key
        resp = self._make_request(api_method, data=data)
        results = resp['tbk_dg_item_coupon_get_response'].get('results', {})
        return results.get('tbk_coupon', [])

    # details
    def item_details(self, item_id):
        if not self.rds_read:
            return []
        item_details_key = '{}{}'.format(self.DETAILS_KEY_PREFIX, item_id)
        item_details_count_key = '{}{}'.format(self.DETAILS_COUNT_KEY_PREFIX,
                                               item_id)
        details = self.rds_read.get(item_details_key) or []
        try:
            details = json.loads(details)
        except Exception:
            details = []
        try:
            count_details = int(self.rds_read.get(item_details_count_key))
        except Exception:
            count_details = 0
        if not details and count_details < self.details_limit:
            self.rds_write.incr(item_details_count_key)
            if not count_details:
                self.rds_write.expire(item_details_count_key, self.expires)
            params = {'data': json.dumps({'item_num_id': item_id})}
            r = requests.get(self.ITEM_DETAILS_BASE_URL, params=params)
            try:
                results = r.json().get('data', {})
                print 'results -->'
                print r.json()
                print r.url
                print 'item_id --->', item_id
                details = results.get('images', [])
            except Exception:
                return []
            item_details_key = '{}{}'.format(self.DETAILS_KEY_PREFIX, item_id)
            try:
                self.rds_write.setex(item_details_key,
                                     json.dumps(details),
                                     self.expires)
            except Exception:
                pass

        return details

    # convert
    def convert(self, item_ids):
        """
        max 40 items, seems require isv.permission.
        """
        api_method = 'taobao.tbk.item.convert'
        fields = [
            'num_iid',
            'click_url'
        ]
        data = {
            'platform': self.platform,
            'adzone_id': self.adzone_id,
            'num_iids': self._list2str(item_ids),
            'fields': ','.join(fields),
        }
        resp = self._make_request(api_method, data=data)
        results = resp['tbk_item_convert_response'].get('results', {})
        return results.get('ntbk_item', [])

    def create_code(self, text, url, logo=None, user_id=None, ext={}):
        api_method = 'taobao.tbk.tpwd.create'
        data = {
            'text': text,
            'url': url,
        }
        if user_id:
            data['user_id'] = user_id
        if logo:
            data['logo'] = logo
        if ext:
            data['ext'] = ext
        resp = self._make_request(api_method, data=data)
        result = resp['tbk_tpwd_create_response'].get('data', {})
        return result.get('model')

    def convert_url(self, url, item_id, activity_id=None, pid=None):
        if not item_id:
            return None
        elif url.startswith(self.CLICK_BASE_URL):
            # TODO: if I can replace click_url
            return None
        elif not url.startswith(self.COUPON_BASE_URL):
            return None

        if not pid:
            pid = self.pid

        if not activity_id:
            activity_id = self._decrypt_activity_id(url)
            if not activity_id:
                # failback to input url when unable to get activity_id.
                return None

        return self._make_coupon_url(activity_id, pid, item_id)

    # helpers
    def _extract_activity_id(self, url):
        try:
            matched = self.ACTID_PATTERN.search(url)
            return matched.groups()[0]
        except Exception:
            return None

    def _decrypt_activity_id(self, coupon_url):
        if not coupon_url.startswith(self.COUPON_BASE_URL):
            return None
        act_id = self._extract_activity_id(coupon_url)
        if act_id:
            return act_id
        restore_url = coupon_url.replace(self.COUPON_BASE_URL,
                                         self.COUPON_RESTORE_API)
        r = requests.get(restore_url)
        try:
            r.raise_for_status()
            result = r.json()
            _url = result['result']['privateCouponUrl']
        except Exception:
            return None
        return self._extract_activity_id(_url)

    def _make_coupon_url(self, activity_id, pid, item_id):
        return '{}?activityId={}&pid={}&itemId={}'.format(
            self.COUPON_BASE_URL, activity_id, pid, item_id)
