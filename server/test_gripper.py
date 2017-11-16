# coding=utf-8
from __future__ import absolute_import

from services.taoke import Taoke


def run_grip():
    # taoke = Taoke(
    #     app_key='24662168',
    #     app_secret='f79192ae6132c08bfea93327891b4d36',
    #     pid='mm_127260061_38528906_142804020',
    #     ssl=False,
    # )
    taoke = Taoke(
        app_key='24662168',
        app_secret='f79192ae6132c08bfea93327891b4d36',
        pid='mm_127260061_38528906_142804020',
        ssl=False,
    )
    results = taoke.list_coupons(search_key=u'连裤袜',
                                 paged=1,
                                 perpage=10)
    print results
    # print taoke.convert('551416224136')

    # results = taoke.list_favorites()
    # print results
    # fav_id = results[0]['favorites_id']
    # results = taoke.list_favorite_items(favorite_id=fav_id, perpage=100)
    # for item in results:
    #     if item.get('coupon_click_url'):
    #         for k, v in item.iteritems():
    #             print k, '----->', v
    #         break
    # paged = 1
    # perpage = 20
    # ids = []

    # for i in xrange(10):
    #     # _count = paged * perpage
    #     # if _count > 100:
    #     #     _perpage = perpage - (_count - 100)
    #     # else:
    #     #     _perpage = perpage
    #     # if _perpage <= 0:
    #     #     break
    #     _perpage = perpage
    #     print 'paged:', paged, '--------------------->'
    #     # _perpage = perpage
    #     results = taoke.list_coupons(search_key=u'连裤袜',
    #                                      paged=paged,
    #                                      perpage=_perpage)
    #     dups = 0
    #     for item in results:
    #         if item['num_iid'] in ids:
    #             # print item['num_iid'], len(ids)
    #             dups += 1
    #         else:
    #             ids.append(item['num_iid'])
    #     paged += 1

    #     print 'results', len(results), '/', _perpage, 'xxx', dups
    #     print '------------------------------>'
    #     # time.sleep(5)

    # print 'total:', len(ids)


if __name__ == '__main__':
    run_grip()
