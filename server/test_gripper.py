# coding=utf-8
from __future__ import absolute_import

from services.taoke import Taoke
import time


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
    # results = taoke.list_favorite_items(favorite_id='13259090', perpage=100)

    paged = 1
    perpage = 60
    ids = []

    for i in xrange(10):
        _count = paged * perpage
        if _count > 100:
            _perpage = perpage - (_count - 100)
        else:
            _perpage = perpage
        if _perpage <= 0:
            break
        print 'paged:', paged, '--------------------->'
        # _perpage = perpage
        results = taoke.list_coupons(search_key=u'巧克力',
                                     paged=paged,
                                     perpage=_perpage)
        dups = 0
        for item in results:
            if item['num_iid'] in ids:
                # print item['num_iid'], len(ids)
                dups += 1
            else:
                ids.append(item['num_iid'])
        paged += 1

        print 'results ---->', len(results), '/', _perpage, 'xxx', dups
        # time.sleep(5)

    print 'total:', len(ids)


if __name__ == '__main__':
    run_grip()
