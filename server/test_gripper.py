# coding=utf-8
from __future__ import absolute_import

from services.taoke import Taoke


def run_grip():
    # taoke = Taoke(
    #     app_key='24656509',
    #     app_secret='b4f67c647b715a74211f688416f613ff',
    #     pid='mm_82570814_38284225_142402853',
    #     ssl=False,
    # )
    taoke = Taoke(
        app_key='24662168',
        app_secret='f79192ae6132c08bfea93327891b4d36',
        pid='mm_127260061_38528906_142804020',
        ssl=False,
    )

    # results = taoke.list_favorites()
    # results = taoke.list_favorite_items(favorite_id='13167987', perpage=100)

    results = taoke.list_coupons(categories='50016422,50002766', perpage=100)
    # print results
    # print 'len:', len(results)

    for item in results:
        if item.get('coupon_info'):
            print item


if __name__ == '__main__':
    run_grip()
