# coding=utf-8
from __future__ import absolute_import

from apiresps.errors import (ValidationError,
                             MethodNotAllowed,
                             InternalServerError,
                             BadRequest,
                             NotFound,
                             Unexpected,
                             ConflictError)


class UserNotFound(NotFound):
    response_code = 700001
    status_message = 'USER_NOT_FOUND'


class UserLoginOccupied(ConflictError):
    status_message = 'USER_LOGIN_OCCUPIED'
    response_code = 700002


class UserNameOccupied(ConflictError):
    status_message = 'USER_NAME_OCCUPIED'
    response_code = 700003


class UserNotActivated(MethodNotAllowed):
    response_code = 700004
    status_message = 'USER_NOT_ACTIVATED'


class UserWrongPassword(BadRequest):
    response_code = 700005
    status_message = 'USER_WRONG_PASSWORD'


class UserPublicRegisterNotAllowed(MethodNotAllowed):
    response_code = 700006
    status_message = 'USER_PUBLIC_REGISTER_NOT_ALLOWED'


class UserCaptchaError(ValidationError):
    response_code = 700007
    status_message = 'USER_CAPTCHA_NOT_MATCH'


class UserCreateFailed(Unexpected):
    response_code = 700008
    status_message = 'USER_CREATE_FAILED'


class UserCreateMailError(InternalServerError):
    response_code = 700009
    status_message = 'USER_CREATE_MAIL_FAILED'


class UserSendMailError(InternalServerError):
    response_code = 700010
    status_message = 'USER_SEND_MAIL_FAILED'


# property
class UserPropertyNotFound(NotFound):
    response_code = 700020
    status_message = 'USER_PROPERTY_NOT_FOUND'
