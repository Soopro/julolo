# coding=utf-8
from __future__ import absolute_import

from flask import (Blueprint,
                   current_app,
                   request,
                   url_for,
                   redirect,
                   flash,
                   render_template)

from mongokit.paginator import Paginator

from utils.misc import parse_int, process_slug
from utils.auth import generate_hashed_password

from admin.decorators import login_required


blueprint = Blueprint('user', __name__, template_folder='pages')


@blueprint.route('/')
@login_required
def index():
    paged = parse_int(request.args.get('paged'), 1, True)
    login = request.args.get('login')
    slug = request.args.get('slug')

    users = current_app.mongodb.User.find_alive(login=login, slug=slug)

    p = Paginator(users, paged, 12)

    prev_url = url_for(request.endpoint,
                       paged=p.previous_page,
                       login=login,
                       slug=slug)
    next_url = url_for(request.endpoint,
                       paged=p.next_page,
                       login=login,
                       slug=slug)

    paginator = {
        'next': next_url if p.has_next else None,
        'prev': prev_url if p.has_previous and p.previous_page else None,
        'paged': p.current_page,
        'start': p.start_index,
        'end': p.end_index,
    }
    return render_template('users.html', users=users, p=paginator)


# @blueprint.route('/inactive')
# @login_required
# def inactive():
#     inactives = []
#     r = current_app.redis
#     keys = r.keys('captcha-register-*')
#     for key in keys:
#         inactive = dict()
#         inactive['login'] = key.split('captcha-register-')[1]
#         inactive['captcha'] = r.get(key)
#         inactives.append(inactive)
#     return render_template('inactive.html', inactives=inactives)


@blueprint.route('/detail')
@blueprint.route('/detail/<user_id>')
@login_required
def detail(user_id=None):
    User = current_app.mongodb.User
    Property = current_app.mongodb.Property
    if user_id:
        user = User.find_one_by_id(user_id)
    else:
        user = {
            'status': User.STATUS_DEACTIVATED
        }

    if user.get('_id'):
        prop = Property.find_one_by_uid(user['_id'])
    else:
        prop = None
    if not prop:
        prop = {
            'pid': u'',
        }

    return render_template('user_detail.html', user=user, prop=prop)


@blueprint.route('/detail', methods=['POST'])
@login_required
def create():
    login = request.form['login']
    passwd = request.form['passwd']
    slug = request.form['slug']
    pid = request.form.get('pid')
    status = request.form.get('status')

    if not pid:
        status = 0

    user = current_app.mongodb.User()
    user['login'] = login
    user['password_hash'] = generate_hashed_password(passwd)
    user['slug'] = process_slug(slug)
    if status is not None:
        user['status'] = parse_int(status)
    user.save()

    prop = current_app.mongodb.Property()
    prop['user_id'] = user['_id']
    prop['pid'] = pid
    prop.save()

    flash('Saved.')
    return_url = url_for('.detail', user_id=user['_id'])
    return redirect(return_url)


@blueprint.route('/detail/<user_id>', methods=['POST'])
@login_required
def update(user_id):
    passwd = request.form.get('passwd')
    status = request.form.get('status')
    pid = request.form.get('pid', u'')

    if not pid:
        status = 0

    user = current_app.mongodb.User.find_one_by_id(user_id)
    if passwd:
        user['password_hash'] = generate_hashed_password(passwd)
    if status is not None:
        user['status'] = parse_int(status)
    user.save()

    prop = current_app.mongodb.Property.find_one_by_uid(user_id)
    if prop['pid'] != pid:
        prop['pid'] = pid
        prop.save()

    flash('Saved.')
    return_url = url_for('.detail', user_id=user['_id'])
    return redirect(return_url)


@blueprint.route('/detail/<user_id>/remove')
@login_required
def remove(user_id):
    user = current_app.mongodb.User.find_one_by_id(user_id)
    user.remove()
    return_url = url_for('.index')
    return redirect(return_url)
