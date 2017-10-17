# coding=utf-8
from __future__ import absolute_import

from flask import (Blueprint,
                   current_app,
                   session,
                   request,
                   redirect,
                   url_for,
                   flash,
                   g,
                   render_template)

from utils.request import get_remote_addr
from utils.misc import hmac_sha

from admin.decorators import login_required


blueprint = Blueprint('admin', __name__, template_folder='pages')

USERNAME = 'admin'
PASSWD = 'facai888$$'


@blueprint.route('/')
@login_required
def index():
    count = {
        'users': current_app.mongodb.User.find_alive().count(),
        'orders': current_app.mongodb.Order.find().count(),
    }
    return render_template('dashboard.html', count=count)


@blueprint.route('/login')
def login():
    g.skip_navs = True
    if session.get('user'):
        return redirect('/')
    return render_template('login.html')


@blueprint.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    pwd = request.form['passwd']
    if username == USERNAME and pwd == PASSWD:
        session['user'] = hmac_sha(current_app.secret_key, get_remote_addr())
        return redirect('/')
    else:
        flash(u'Wrong username or password!')
        return redirect(url_for('.login'))


@blueprint.route('/logout')
@login_required
def logout():
    session.pop('user', None)
    return redirect(url_for('.login'))
