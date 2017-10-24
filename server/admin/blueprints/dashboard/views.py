# coding=utf-8
from __future__ import absolute_import

from flask import (Blueprint,
                   current_app,
                   render_template)


from admin.decorators import login_required


blueprint = Blueprint('base', __name__, template_folder='pages')


@blueprint.route('/')
@login_required
def index():
    total = current_app.sa_mod.get_total_customer()
    days = current_app.sa_mod.get_days_customer()
    count = {
        'total': total,
        'days': days,
    }
    return render_template('dashboard.html', count=count)
