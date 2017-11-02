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
import os
from zipfile import ZipFile

from utils.model import make_paginator
from utils.files import ensure_dirs, remove_dirs
from utils.request import get_args
from utils.misc import to_timestamp, now, parse_int

from admin.decorators import login_required

blueprint = Blueprint('commodity', __name__, template_folder='pages')


@blueprint.route('/')
@login_required
def index():
    paged = parse_int(get_args('paged'), 1, True)
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
    file = request.files['file']

    tmp_base_dir = current_app.config.get('TEMPORARY_FOLDER')
    upload_dir = os.path.join(tmp_base_dir, 'commodities', str(now()))
    remove_dirs(upload_dir)
    ensure_dirs(upload_dir)

    with ZipFile(file) as z:
        z.extractall(upload_dir)

    file_path = None
    for f in os.listdir(upload_dir):
        if f.endswith(".json"):
            file_path = os.path.join(upload_dir, f)
            break
    if not file_path:
        msg = u'invalid commodities file, must be a .json in .zip pack.'
        raise Exception(msg)

    with open(file_path) as f:
        items_str = f.read()
        items_list = json.loads(items_str)

    remove_dirs(upload_dir)

    count = 0
    for item in items_list:
        if current_app.mongodb.Commodity.find_one_by_itemid(item['item_id']):
            continue
        commodity = current_app.mongodb.Commodity()
        commodity['item_id'] = item['item_id']
        commodity['shop'] = item['shop']
        commodity['type'] = 1 if item['type'] == u'天猫' else 0
        commodity['title'] = item['title']
        commodity['src'] = item['src']
        commodity['volume'] = item['volume']
        commodity['price'] = parse_int(item['price'] * 100)
        commodity['income_rate'] = parse_int(item['income_rate'] * 100)
        commodity['commission'] = parse_int(item['commission'] * 100)
        commodity['coupon'] = item['coupon']
        commodity['start_time'] = to_timestamp(item['start_time'])
        commodity['end_time'] = to_timestamp(item['end_time'])
        commodity['click_url'] = item['click_url']
        commodity['coupon_click_url'] = item['coupon_click_url']
        commodity.save()
        count += 1

    flash('{} Commodities updated.'.format(count))
    return_url = url_for('.index')
    return redirect(return_url)
