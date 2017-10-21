# coding=utf-8
from __future__ import absolute_import

from services.taoke import Taoke


def run_grip():
    taoke = Taoke(
        app_key='24656509',
        app_secret='b4f67c647b715a74211f688416f613ff',
        pid='mm_82570814_38284225_142402853',
        ssl=False,
    )

    # results = taoke.list_favorites()

    results = taoke.list_favorite_items(favorite_id='12968308', perpage=100)
    # results = taoke.list_favorite_items(favorite_id='12968308', perpage=100)

    # results = taoke.list_coupons(categories=[2813], perpage=100)
    # print results
    # print 'len:', len(results)

    for item in results:
        if item.get('coupon_info'):
            print item


if __name__ == '__main__':
    run_grip()
