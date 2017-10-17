# coding=utf-8
from __future__ import absolute_import

from flask import current_app, request
from werkzeug.security import generate_password_hash, check_password_hash

import hashlib
import hmac

from datetime import timedelta
from bson import ObjectId
from itsdangerous import (TimedJSONWebSignatureSerializer,
                          JSONWebSignatureSerializer,
                          SignatureExpired,
                          BadSignature)

from apiresps.errors import AuthFailed


def get_timed_serializer(expires_in=None, salt='supmice'):
    if not isinstance(salt, basestring):
        salt = 'supmice'

    if expires_in is None:
        expires_in = current_app.config.get('JWT_EXPIRATION_DELTA', 0)
    if isinstance(expires_in, timedelta):
        expires_in = int(expires_in.total_seconds())
    expires_in_total = expires_in + current_app.config.get('JWT_LEEWAY', 0)

    return TimedJSONWebSignatureSerializer(
        secret_key=current_app.config.get('JWT_SECRET_KEY'),
        expires_in=expires_in_total,
        salt=salt,
        algorithm_name=current_app.config.get('JWT_ALGORITHM', 'HS256'))


def get_serializer(salt='supmice'):
    if not isinstance(salt, basestring):
        salt = 'supmice'

    return JSONWebSignatureSerializer(
        secret_key=current_app.config.get('JWT_SECRET_KEY'),
        salt=salt,
        algorithm_name=current_app.config.get('JWT_ALGORITHM', 'HS256'))


def load_token():
    key = current_app.config['JWT_AUTH_HEADER_KEY']
    prefix = current_app.config['JWT_AUTH_HEADER_PREFIX']
    auth = request.headers.get(key, None)

    if auth is None:
        raise AuthFailed('Authorization Required')

    parts = auth.split()

    if parts[0].lower() != prefix.lower():
        raise AuthFailed('Invalid JWT header' 'Unsupported authorization')
    elif len(parts) == 1:
        raise AuthFailed('Invalid JWT header' 'Token missing')
    elif len(parts) > 2:
        raise AuthFailed('Invalid JWT header' 'Token contains spaces')
    return parts[1]


def load_payload(payload, timed=True, salt=None):
    try:
        if timed:
            return get_timed_serializer(salt=salt).loads(payload)
        else:
            return get_serializer(salt=salt).loads(payload)
    except SignatureExpired:
        raise AuthFailed('Invalid JWT' 'Token is expired')
    except BadSignature:
        raise AuthFailed('Invalid JWT' 'Token is undecipherable')


def get_jwt_token():
    try:
        auth = request.headers.get('Authorization')
        parts = auth.split()
        token = parts[1]
    except Exception:
        token = ''
    return token


def generate_token(payload, expires_in=None, salt=None):
    if not isinstance(payload, (dict, list)):
        payload = unicode(payload)
    ts = get_timed_serializer(expires_in=expires_in, salt=salt)
    return ts.dumps(payload).decode('utf-8')


def generate_sid(payload, expires_in=None, salt=None):
    return generate_token(payload, expires_in, salt)


def generate_hashed_password(password):
    return unicode(generate_password_hash(unicode(password)))


def check_hashed_password(hashed, password):
    return check_password_hash(str(hashed), password)
