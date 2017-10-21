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


blueprint = Blueprint('auth', __name__, template_folder='pages')


@blueprint.route('/login')
def login():
    if session.get('user'):
        return redirect('/')
    return render_template('login.html')


@blueprint.route('/login', methods=['POST'])
def do_login():
    admin_code = current_app.config.get('ADMIN_CODE')
    identity = u'hys{}'.format(admin_code)
    if request.form['passcode'] == identity:
        session['user'] = hmac_sha(current_app.secret_key,
                                   get_remote_addr())
        return redirect('/')
    else:
        flash('Wrong passcode')
        return redirect(url_for('.login'))


@blueprint.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('.login'))
