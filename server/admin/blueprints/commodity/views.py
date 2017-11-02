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
from zipfile import ZipFile
import csv

from utils.files import ensure_dirs, remove_dirs
from utils.misc import safe_filename, now

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
    file = request.files['file']

    return_url = url_for('.index')
    tmp_base_dir = current_app.config['TEMPORARY_FOLDER']
    upload_dir = os.path.join(tmp_base_dir, 'commodity', str(now()))
    remove_dirs(upload_dir)
    ensure_dirs(upload_dir)

    filename = safe_filename(file.filename)
    fname, ext = os.path.splitext(filename)

    if ext != '.zip':
        flash('Must be .zip file contain a .csv.', 'error')
        return redirect(return_url)

    # unpack file
    with ZipFile(file) as z:
        z.extractall(upload_dir)

    csv_path = os.path.join(upload_dir, fname)
    if not os.path.isfile(csv_path):
        flash('A zip file contain a .csv file with same name', 'error')
        return redirect(return_url)

    def _convert_unicode(input):
        if not isinstance(input, unicode):
            return input.decode('utf-8')
        else:
            return input

    commodities = []
    with open(csv_path, 'rb') as csvfile:
        readered = csv.reader(csvfile)
        for row in readered:
            commodities.append({
                'item_id': int(row[0]),
                'title': _convert_unicode(row[1]),
                'src': _convert_unicode(row[2]),
                'detail_url': _convert_unicode(row[3]),
                'category_name': _convert_unicode(row[4]),
                'click_url': _convert_unicode(row[5]),
                'price': float(row[6]),
                'volume': int(row[7]),
                'income_rate': float(row[8]),
                'commission': float(row[9]),
                'seller_im': _convert_unicode(row[10]),
                'seller_id': _convert_unicode(row[11]),
                'shop': _convert_unicode(row[12]),
                'type': _convert_unicode(row[13]),
                'coupon_id': _convert_unicode(row[14]),
                'coupon_volume': int(row[15]),
                'coupon_remine': int(row[16]),
                'coupon': _convert_unicode(row[17]),
                'start_time': _convert_unicode(row[18]),
                'end_time': _convert_unicode(row[19]),
                'coupon_url': _convert_unicode(row[20]),
                'coupon_click_url': _convert_unicode(row[21]),
            })
    for k, v in commodities[-1].iteritems():
        print v
    flash('Commodities updated.')
    return redirect(return_url)
