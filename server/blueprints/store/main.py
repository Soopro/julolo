# coding=utf-8
from __future__ import absolute_import

from flask import Blueprint

from apiresps.errors import APIError

from utils.misc import route_inject
from utils.response import make_json_response

from ..inspection import verify_access

from .routes import urlpatterns


bp_name = 'store'

blueprint = Blueprint(bp_name, __name__)

route_inject(blueprint, urlpatterns)

# endpoint types
open_api_endpoints = [
    '{}.get_store'.format(bp_name),
    '{}.list_commodities'.format(bp_name),
    '{}.get_commodity'.format(bp_name),
    '{}.search_commodities'.format(bp_name),
    '{}.list_item_coupons'.format(bp_name),
    '{}.search_item_coupons'.format(bp_name),
    '{}.generate_coupon_code'.format(bp_name),
    '{}.list_categories'.format(bp_name),
    '{}.get_category'.format(bp_name),
    '{}.list_promotions'.format(bp_name),
    '{}.get_promotion'.format(bp_name),
    '{}.list_promotion_items'.format(bp_name),
    '{}.list_shortcuts'.format(bp_name),
    '{}.get_shortcut'.format(bp_name),
    '{}.list_tips'.format(bp_name),
]


@blueprint.before_request
def before():
    verify_access(
        open_api=open_api_endpoints
    )


@blueprint.errorhandler(APIError)
def blueprint_api_err(err):
    return make_json_response(err)
