# coding=utf-8
from __future__ import absolute_import

from flask import current_app, g

from utils.auth import (generate_token,
                        get_jwt_token,
                        generate_hashed_password,
                        check_hashed_password)

from utils.response import output_json
from utils.request import get_param
from utils.misc import (process_slug, now)

from helpers.captcha import (set_captcha,
                             check_captcha,
                             del_captcha)

from helpers.identity import get_user_hmac_sha

from apiresps.validations import Struct

from ..helpers import (helper_send_register_email,
                       helper_send_recovery_email,
                       helper_get_user_by_login)
from ..errors import (UserLoginOccupied,
                      UserNameOccupied,
                      UserWrongPassword,
                      UserCaptchaError)


CAPTCHA_REGISTER = 'register'
CAPTCHA_RECOVERY = 'recovery'


@output_json
def register_captcha():
    login = get_param('login', Struct.Login, True)
    locale = get_param('locale', Struct.Attr)

    login = login.lower()
    user = current_app.mongodb.User.find_one_by_login(login)
    if user is not None:
        raise UserLoginOccupied

    expires_in = current_app.config.get('REGISTER_EXPIRATION')
    captcha = set_captcha(CAPTCHA_REGISTER, login, expires_in)

    # email
    helper_send_register_email(login, captcha, expires_in, locale)

    if current_app.debug is True:
        checked = captcha
    else:
        checked = True

    return {
        'login': login,
        'checked': checked,
    }


@output_json
def register():
    captcha = get_param('captcha', Struct.Attr, True)
    login = get_param('login', Struct.Login, True)
    passwd = get_param('passwd', Struct.Pwd, True)
    slug = get_param('slug', Struct.Attr, True)
    meta = get_param('meta', Struct.Dict, default={})

    login = login.lower()
    slug = process_slug(slug)

    User = current_app.mongodb.User

    user = User.find_one_by_login(login)
    if user is not None:
        raise UserLoginOccupied

    if not check_captcha(CAPTCHA_REGISTER, login, captcha):
        raise UserCaptchaError

    if User.find_one_by_slug(slug) is not None:
        raise UserNameOccupied

    del_captcha(CAPTCHA_REGISTER, login)

    user = User()
    user['login'] = login
    user['slug'] = slug
    user['meta'] = meta
    user['password_hash'] = generate_hashed_password(passwd)
    user['status'] = User.STATUS_ACTIVATED
    user.save()

    token = generate_token({
        'user_id': str(user['_id']),
        'sha': get_user_hmac_sha(user),
    })

    return {
        'login': user['login'],
        'slug': user['slug'],
        'token': token,
        'id': user['_id'],
        'updated': user['updated'],
        'status': user['status'],
    }


@output_json
def login():
    login = get_param('login', Struct.Login, True)
    passwd = get_param('passwd', Struct.Pwd, True)

    user = helper_get_user_by_login(login)

    pass_checked = check_hashed_password(str(user['password_hash']), passwd)
    if pass_checked is not True:
        raise UserWrongPassword

    token = generate_token({
        'user_id': str(user['_id']),
        'sha': get_user_hmac_sha(user),
    })

    return {
        'id': user['_id'],
        'login': user['login'],
        'slug': user['slug'],
        'updated': user['updated'],
        'status': user['status'],
        'token': token
    }


@output_json
def logout():
    token = get_jwt_token()
    if token:
        prefix = current_app.config.get('INVALID_USER_TOKEN_PREFIX')
        expire = current_app.config.get('JWT_EXPIRATION_DELTA')
        current_app.redis.setex('{}{}'.format(prefix, token), True, expire)

    return {
        'token': None,
        'updated': now(),
    }


@output_json
def recovery_captcha():
    login = get_param('login', Struct.Login, True)
    locale = get_param('locale', Struct.Attr)

    user = helper_get_user_by_login(login)

    expires_in = current_app.config.get('RESET_PWD_EXPIRATION')
    captcha = set_captcha(CAPTCHA_RECOVERY, user['login'], expires_in, 24)

    # email
    helper_send_recovery_email(user, captcha, expires_in, locale)

    if current_app.debug is True:
        recovered = captcha
    else:
        recovered = True

    return {
        'login': user['login'],
        'recovered': recovered,
    }


@output_json
def recovery():
    captcha = get_param('captcha', Struct.Attr, True)
    login = get_param('login', Struct.Login, True)
    passwd = get_param('passwd', Struct.Pwd, True)

    user = helper_get_user_by_login(login)
    if not check_captcha(CAPTCHA_RECOVERY, user['login'], captcha):
        raise UserCaptchaError

    del_captcha(CAPTCHA_RECOVERY, user['login'])

    new_hash = generate_hashed_password(passwd)
    user['password_hash'] = new_hash
    user.save()

    return {
        'id': user['_id'],
        'updated': user['updated'],
    }


@output_json
def update_password():
    passwd = get_param('passwd', Struct.Pwd, True)
    old_passwd = get_param('old_passwd', Struct.Pwd, True)

    user = g.user
    pass_checked = check_hashed_password(str(user['password_hash']),
                                         old_passwd)
    if pass_checked is not True:
        raise UserWrongPassword

    user['password_hash'] = generate_hashed_password(passwd)
    user.save()

    token = generate_token({
        'user_id': str(user['_id']),
        'sha': get_user_hmac_sha(user),
    })

    return {
        'id': user['_id'],
        'token': token,
        'updated': user['updated'],
    }


@output_json
def get_profile():
    user = g.user
    return output_profile(user)


@output_json
def update_profile():
    meta = get_param('meta', Struct.Dict, default={})

    user = g.user
    user['meta'] = meta
    user.save()
    return output_profile(user)


# outputs
def output_profile(user):
    return {
        'id': user['_id'],
        'login': user['login'],
        'slug': user['slug'],
        'meta': user['meta'],
        'status': user['status'],
        'updated': user['updated'],
    }
