# coding=utf-8
from __future__ import absolute_import

from flask import (Blueprint,
                   current_app,
                   request,
                   url_for,
                   redirect,
                   flash,
                   render_template)
import os
import json
from zipfile import ZipFile

from utils.model import make_paginator
from utils.request import get_args
from utils.files import remove_dirs
from utils.misc import (to_timestamp,
                        split_file_ext,
                        process_slug,
                        parse_int,
                        uuid4_hex,
                        now)

from admin.decorators import login_required

blueprint = Blueprint('commodity', __name__, template_folder='pages')


@blueprint.route('/')
@login_required
def index():
    paged = parse_int(get_args('paged'), 1, True)
    last_filename = get_args('last')
    commodities = current_app.mongodb.Commodity.find_all()
    activities = current_app.mongodb.Activity.find_all()

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
                           activities=activities,
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
    activity = request.form.get('activity', u'')

    ext = split_file_ext(f.filename)
    if ext == 'json':
        items_list = json.loads(f.stream.read())
    elif ext == 'zip':
        items_list = _unpack_items(f)
    else:
        raise Exception('must be json or zip')

    new_count = 0
    update_count = 0

    for item in items_list:
        item_id = unicode(item['item_id'])
        start_time = to_timestamp(item['coupon_start_time'])
        end_time = to_timestamp(item['coupon_end_time'])

        if now() >= (end_time + 3600 * 6):
            continue

        commodity = current_app.mongodb.\
            Commodity.find_one_by_itemid(item_id)

        if not commodity:
            commodity = current_app.mongodb.Commodity()
            commodity['item_id'] = item_id
            new_count += 1
        else:
            update_count += 1

        commodity['cid'] = unicode(item['cid'])
        commodity['shop_type'] = item['shop_type']
        commodity['shop_title'] = item['shop_title']
        commodity['title'] = item['title']
        commodity['src'] = item['pic_url']

        if item['volume']:  # incase volume not provided (with 0).
            commodity['volume'] = item['volume']

        commodity['activity'] = process_slug(activity, False)
        commodity['price'] = parse_int(item['price'] * 100)
        commodity['income_rate'] = parse_int(item['income_rate'] * 100)
        commodity['commission'] = parse_int(item['commission'] * 100)

        if item['coupon_id']:  # incase coupon_id is missing with activity.
            commodity['coupon_id'] = item['coupon_id']

        commodity['coupon_info'] = item['coupon_info']
        commodity['category'] = item['category']

        commodity['start_time'] = start_time
        commodity['end_time'] = end_time
        commodity['click_url'] = item['click_url']
        commodity['coupon_url'] = item['coupon_url']
        commodity['coupon_click_url'] = item['coupon_click_url']
        commodity['memo'] = item['memo']
        commodity.save()

    flash('{} Commodities added, {} updated.'.format(new_count, update_count))

    return_url = url_for('.index', last=f.filename)
    return redirect(return_url)


def _unpack_items(zipped_items):
    items_list = []
    tmp_base_dir = current_app.config.get('TEMPORARY_FOLDER')
    tmp_dir = os.path.join(tmp_base_dir, 'commodity', uuid4_hex())
    try:
        with ZipFile(zipped_items) as z:
            z.extractall(tmp_dir)

        for path in os.listdir(tmp_dir):
            file_path = os.path.join(tmp_dir, path)
            with open(file_path) as f:
                items = json.loads(f.read())
                items_list += items
    except Exception as e:
        remove_dirs(tmp_dir)
        raise e

    remove_dirs(tmp_dir)

    return items_list
