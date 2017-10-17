# coding=utf-8
from .controllers import *

urlpatterns = [
    # # register
    # ('/register', register, 'POST'),  # open api
    # ('/register/captcha', register_captcha, 'POST'),  # open api

    # # recovery
    # ('/recovery', recovery, 'POST'),  # open api
    # ('/recovery/captcha', recovery_captcha, 'POST'),  # open api

    # auth
    ('/auth', login, 'POST'),  # open api
    ('/auth', logout, 'DELETE'),

    # security
    ('/security', update_password, 'PUT'),

    # profile
    ('/profile', get_profile, 'GET'),
    ('/profile', update_profile, 'PUT'),

    # property
    ('/property', get_property, 'GET'),

]
