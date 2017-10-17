# coding=utf-8
from __future__ import absolute_import

import hashlib
import time
import requests


class Taoke(object):
    API_BASE = 'gw.api.taobao.com/router/rest'

    protocol = 'http'

    headers = {
        'Content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'Cache-Control': 'no-cache',
        'Connection': 'Keep-Alive',
    }
    app_key = None
    app_secret = None
    adzone_id = None
    pid = None

    platform = 2  # 1: pc, 2: mobile
    timeout = 30

    def __init__(self, app_key, app_secret, pid,
                 platform=2, ssl=True, timeout=30):
        self.app_key = app_key
        self.app_secret = app_secret
        self.pid = pid
        self.adzone_id = pid.split('_')[-1]
        self.platform = platform
        self.timeout = timeout

        self.protocol = 'https' if ssl else 'http'
        self.API_URL = u'{}://{}'.format(self.protocol, self.API_BASE)

    def _sign(self, req_params):
        keys = req_params.keys()
        keys.sort()

        params_str = ''.join('%s%s' % (key, req_params[key]) for key in keys)
        pm_str = '{secret}{params}{secret}'.format(secret=self.app_secret,
                                                   params=params_str)
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
        for item in iters:
            try:
                _list.append(str(item))
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
        try:
            results = resp['tbk_uatm_favorites_get_response']['results']
            return results['tbk_favorites']
        except Exception:
            raise Exception(resp)

    def list_favorite_items(self, favorites_id, paged=1, perpage=12):
        api_method = 'taobao.tbk.uatm.favorites.item.get'
        fields = [
            'num_iid',
            'title',
            'pict_url',
            'small_images',
            'reserve_price',
            'zk_final_price',
            'user_type',
            'provcity',
            'item_url',
            'seller_id',
            'volume',
            'nick',
            'shop_title',
            'zk_final_price_wap',
            'event_start_time',
            'event_end_time',
            'tk_rate',
            'status',
            'type',
        ]
        data = {
            'platform': self.platform,
            'adzone_id': self.adzone_id,
            'favorites_id': favorites_id,
            'page_no': paged,
            'page_size': perpage,
            'fields': ','.join(fields),
        }
        return self._make_request(api_method, data=data)

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
            data['cat'] = self._list2str(categories)
        if search_key:
            data['q'] = search_key
        resp = self._make_request(api_method, data=data)
        try:
            results = resp['tbk_dg_item_coupon_get_response']['results']
            return results['tbk_coupon']
        except Exception:
            raise Exception(resp)
