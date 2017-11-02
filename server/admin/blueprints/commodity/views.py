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

from utils.misc import to_timestamp

from admin.decorators import login_required

blueprint = Blueprint('commodity', __name__, template_folder='pages')


@blueprint.route('/')
@login_required
def index():
    commodities = current_app.mongodb.Commodity.find_all()
    return render_template('commodities.html', commodities=commodities)


@blueprint.route('/upload', methods=['POST'])
@login_required
def upload():
    return_url = url_for('.index')

    try:
        f = request.files['file']
        item_list = json.loads(f.stream.read())
    except Exception:
        flash('Invalid commodities file, must be .json', 'error')
        return redirect(return_url)

    count = 0
    for item in item_list:
        commodity = current_app.mongodb.Commodity()
        commodity['item_id'] = item['item_id']
        commodity['shop'] = item['shop']
        commodity['type'] = 1 if item['type'] == u'天猫' else 0
        commodity['title'] = item['title']
        commodity['src'] = item['src']
        commodity['volume'] = item['volume']
        commodity['income_rate'] = item['income_rate']
        commodity['commission'] = item['commission']
        commodity['coupon'] = item['coupon']
        commodity['start_time'] = to_timestamp(item['start_time'])
        commodity['end_time'] = to_timestamp(item['end_time'])
        commodity['click_url'] = item['click_url']
        commodity['coupon_click_url'] = item['coupon_click_url']
        commodity.save()
        count += 1

    flash('{} Commodities updated.'.format(count))
    return redirect(return_url)
