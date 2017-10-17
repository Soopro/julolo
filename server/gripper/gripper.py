# coding=utf-8
from __future__ import absolute_import

from mongokit import Connection as MongodbConn

import traceback
import logging
import time

from config import config

from common_models import Coupon

from services.taoke import Taoke

from envs import CONFIG_NAME


models = [Coupon]


def start_gripper(options, mongodb):
    taoke = Taoke(
        app_key=options['app_key'],
        app_secret=options['app_secret'],
        pid=options['pid'],
        ssl=options.get('ssl')
    )
    # taoke = Taoke(
    #     app_key='24626487',
    #     app_secret='50f652df4bb5eb11775c71ecf5c87b07',
    #     pid='mm_24208218_36622239_131138849',
    #     ssl=options.get('ssl'),
    # )

    # results = taoke.list_favorites(perpage=100)

    results = taoke.list_coupons(categories=[2813], perpage=100)
    print results
    print 'len:', len(results)
    # while has_more:
    #     coupons = taoke.list_coupons(paged=paged, perpage=100)
    #     if coupons:
    #         _record_coupons(coupons, mongodb)
    #     else:
    #         has_more = False


# def _record_coupons(coupons, mongodb):
#     for pon in coupons:
#         item_id = pon.get('num_iid')
#         if not item_id:
#             continue
#         coupon = mongodb.Coupon.find_one_by_itemid(item_id)
#         if not coupon:
#             coupon = mongodb.Coupon()
#         coupon['item_id'] = item_id
#         coupon['shop_id'] = pon['seller_id']
#         coupon['shop'] = pon['shop_title']
#         time.sleep(0.5)


def run(config_name='default'):
    config_name = CONFIG_NAME or config_name
    cfg = config[config_name]

    mongodb_conn = MongodbConn(
        host=cfg.MONGODB_HOST,
        port=cfg.MONGODB_PORT,
        max_pool_size=cfg.MONGODB_MAX_POOL_SIZE,
    )

    mongodb_conn.register(models)

    mongodb = mongodb_conn[cfg.MONGODB_DATABASE]
    if hasattr(cfg, 'MONGODB_USER') and \
       hasattr(cfg, 'MONGODB_PASSWORD') and \
       cfg.MONGODB_USER and cfg.MONGODB_PASSWORD:
        mongodb.authenticate(cfg.MONGODB_USER, cfg.MONGODB_PASSWORD)

    start_gripper(cfg.TAOKE, mongodb)
