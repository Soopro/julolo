# coding=utf-8
from __future__ import absolute_import

from flask import Blueprint

from apiresps.errors import APIError

from utils.misc import route_inject
from utils.response import make_json_response

from ..inspection import verify_access

from .routes import urlpatterns


bp_name = 'goods'

blueprint = Blueprint(bp_name, __name__)

route_inject(blueprint, urlpatterns)

# endpoint types
open_api_endpoints = [
    '{}.list_coupons'.format(bp_name),
    '{}.search_coupons'.format(bp_name),
]


@blueprint.before_request
def before():
    verify_access(
        open_api=open_api_endpoints
    )


@blueprint.errorhandler(APIError)
def blueprint_api_err(err):
    return make_json_response(err)
