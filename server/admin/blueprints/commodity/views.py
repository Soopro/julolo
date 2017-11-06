# coding=utf-8
from __future__ import absolute_import

from flask import (Blueprint,
                   current_app,
                   request,
                   url_for,
                   redirect,
                   flash,
                   render_template)

import json

from utils.model import make_paginator
from utils.request import get_args
from utils.misc import to_timestamp, parse_int

from admin.decorators import login_required

blueprint = Blueprint('commodity', __name__, template_folder='pages')


@blueprint.route('/')
@login_required
def index():
    paged = parse_int(get_args('paged'), 1, True)
    last_filename = get_args('last')
    commodities = current_app.mongodb.Commodity.find_all()
    p = make_paginator(commodities, paged, 60)
    prev_url = url_for(request.endpoint,
                       paged=p.previous_page)
    next_url = url_for(request.endpoint,
                       paged=p.next_page)

    paginator = {
        'next': next_url if p.has_next else None,
        'prev': prev_url if p.has_previous and p.previous_page else None,
        'paged': p.current_page,
        'start': p.start_index,
        'end': p.end_index,
        'count': p.count,
    }
    if last_filename:
        flash('Last file is: {}'.format(last_filename))
    return render_template('commodities.html',
                           commodities=commodities,
                           p=paginator)


@blueprint.route('/<cmdt_id>/remove')
@login_required
def remove(cmdt_id):
    commodity = current_app.mongodb.Commodity.find_one_by_id(cmdt_id)
    commodity.delete()
    flash('Commodity removed.')
    return_url = url_for('.index')
    return redirect(return_url)


@blueprint.route('/clear')
@login_required
def clear():
    current_app.mongodb.Commodity.clear_expired()
    flash('Commodity cleared.')
    return_url = url_for('.index')
    return redirect(return_url)


@blueprint.route('/upload', methods=['POST'])
@login_required
def upload():
    f = request.files['file']
    items_list = json.loads(f.stream.read())

    count = 0
    for item in items_list:
        if current_app.mongodb.Commodity.find_one_by_itemid(item['item_id']):
            continue
        commodity = current_app.mongodb.Commodity()
        commodity['item_id'] = item['item_id']
        commodity['shop_type'] = item['shop_type']
        commodity['shop_title'] = item['shop_title']
        commodity['title'] = item['title']
        commodity['src'] = item['pic_url']
        commodity['volume'] = item['volume']
        commodity['price'] = parse_int(item['price'] * 100)
        commodity['income_rate'] = parse_int(item['income_rate'] * 100)
        commodity['commission'] = parse_int(item['commission'] * 100)
        commodity['coupon_info'] = item['coupon_info']
        commodity['category'] = item['category']
        commodity['cid'] = parse_int(item['cid'], -1)
        commodity['start_time'] = to_timestamp(item['coupon_start_time'])
        commodity['end_time'] = to_timestamp(item['coupon_end_time'])
        commodity['click_url'] = item['click_url']
        commodity['coupon_click_url'] = item['coupon_click_url']
        commodity.save()
        count += 1

    flash('{} Commodities updated.'.format(count))
    return_url = url_for('.index', last=f.filename)
    return redirect(return_url)
