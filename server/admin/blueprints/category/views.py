# coding=utf-8
from __future__ import absolute_import

from flask import (Blueprint,
                   current_app,
                   request,
                   url_for,
                   redirect,
                   flash,
                   render_template)

from utils.misc import uuid4_hex

from admin.decorators import login_required

blueprint = Blueprint('category', __name__, template_folder='pages')


@blueprint.route('/')
@login_required
def index():
    categories = current_app.mongodb.Category.find_all()
    return render_template('cat_list.html', categories=categories)


@blueprint.route('/create')
@login_required
def create():
    category = current_app.mongodb.Category()
    category['slug'] = uuid4_hex(12)
    category.save()

    flash('Created.')
    return_url = url_for('.detail', cat_id=category['_id'])
    return redirect(return_url)


@blueprint.route('/detail/<cat_id>')
@login_required
def detail(cat_id):
    category = current_app.mongodb.Category.find_one_by_id(cat_id)
    return render_template('cat_detail.html', category=category)


@blueprint.route('/detail/<cat_id>', methods=['POST'])
@login_required
def update(cat_id):
    title = request.form['title']
    poster = request.form['poster']
    favorite_id = request.form['favorite_id']
    priority = request.form['priority']
    status = request.form.get('status')

    category = current_app.mongodb.Category.find_one_by_id(cat_id)
    category['poster'] = poster
    category['title'] = title
    category['favorite_id'] = favorite_id
    category['priority'] = int(priority)
    category['status'] = int(status) if favorite_id else 0
    category.save()

    flash('Saved.')
    return_url = url_for('.detail', cat_id=category['_id'])
    return redirect(return_url)


@blueprint.route('/detail/<cat_id>/remove')
@login_required
def remove(cat_id):
    category = current_app.mongodb.Category.find_one_by_id(cat_id)
    category.delete()
    return_url = url_for('.index')
    return redirect(return_url)
