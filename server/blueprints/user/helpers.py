# coding=utf-8
from __future__ import absolute_import

from flask import current_app
from jinja2 import Template

from matters import RegisterMatter, RecoveryMatter

from .errors import (UserNotFound,
                     UserNotActivated,
                     UserSendMailError,
                     UserCreateMailError,
                     UserPropertyNotFound)


def helper_get_user_by_login(login):
    User = current_app.mongodb.User
    user = User.find_one_by_login(login.lower())
    if user is None:
        raise UserNotFound
    elif user['status'] != User.STATUS_ACTIVATED:
        raise UserNotActivated
    return user


def helper_send_register_email(login, captcha, expires_in, locale):
    recipients = [login]
    reg_matter = RegisterMatter(locale)
    template = reg_matter.output().get('template')
    subject = reg_matter.output().get('subject')

    context = {
        'captcha': captcha or '',
        'expires_in': expires_in or 0,
        'login': login
    }

    try:
        content = Template(template).render(**context)
    except Exception as e:
        raise UserCreateMailError(str(e))

    # send mail
    _send_mail(recipients, subject, content)
    return


def helper_send_recovery_email(user, captcha, expires_in, locale):
    recipients = [user['login']]
    rec_matter = RecoveryMatter(locale)
    template = rec_matter.output().get('template')
    subject = rec_matter.output().get('subject')

    context = {
        'captcha': captcha or '',
        'expires_in': expires_in or 0,
        'meta': user['meta'],
        'login': user['login']
    }

    try:
        content = Template(template).render(**context)
    except Exception as e:
        raise UserCreateMailError(str(e))

    # send mail
    _send_mail(recipients, subject, content)
    return


def _send_mail(recipients, subject, content):
    # send mail
    if not current_app.config.get('SEND_MAIL'):
        return
    try:
        current_app.mail_sender.send(recipients, subject, content)
    except Exception as e:
        current_app.logger.warn(e)
        raise UserSendMailError(str(e))
    return True


# property
def helper_get_property(user):
    prop = current_app.mongodb.Property.find_one_by_uid(user['_id'])
    if not prop:
        raise UserPropertyNotFound
    return prop
