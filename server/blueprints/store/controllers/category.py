# coding=utf-8
from __future__ import absolute_import

from flask import current_app

from utils.response import output_json

from helpers.media import media_safe_src

from ..errors import StoreCategoryNotFound


@output_json
def list_categories():
    categories = current_app.mongodb.Category.find_activated()
    return [output_category(cat) for cat in categories]


@output_json
def get_category(cat_slug):
    category = current_app.mongodb.Category.find_one_by_slug(cat_slug)
    if not category:
        raise StoreCategoryNotFound
    return output_category(category)


# outputs
def output_category(category):
    return {
        'id': category['_id'],
        'slug': category['slug'],
        'label': category['label'],
        'title': category['title'],
        'caption': category['caption'],
        'cat_ids': category['cat_ids'],
        'icon': media_safe_src(category['icon'], category['updated']),
        'updated': category['updated'],
        'creation': category['creation'],
    }
