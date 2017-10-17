# coding=utf-8
from __future__ import absolute_import


class BaseMatter(object):
    SUBJECT = {
        'en': u'TaokeBao',
        'zh': u'淘客宝',
    }
    TEMPLATE = {
        'en': u'Welcome!',
        'zh': u'欢迎！',
    }

    _locale = None

    def __init__(self, locale):
        if not isinstance(locale, basestring):
            locale = 'en'
        self._locale = locale

    def _translate(self, tmpl_dict, locale):
        if isinstance(tmpl_dict, basestring):
            return tmpl_dict
        elif not isinstance(tmpl_dict, dict):
            return u''
        tmpl = tmpl_dict.get(locale)
        if not tmpl:
            lang = locale.split('_')[0]
            tmpl = tmpl_dict.get(lang)
        if not tmpl:
            for item in tmpl_dict.iteritems():
                tmpl = item
                break
        return tmpl or u''

    def output(self):
        subject = self._translate(self.SUBJECT, self._locale)
        template = self._translate(self.TEMPLATE, self._locale)

        return {
            'subject': subject,
            'template': template,
        }


class RegisterMatter(BaseMatter):

    SUBJECT = {
        'en': u'TaokeBao: Activation',
        'zh': u'淘客宝：帐号激活',
    }
    TEMPLATE = {
        'en': u''.join([
            u'<h1>Your account is ready!</h1>',
            u'<p>Please use the Captcha below to finish activation.</p>'
            u'<p>There is the Captcha code:</p>',
            u'<p style="font-size:36px;">{{captcha}}</p>'
        ]),

        'zh': u''.join([
            u'<h1>您的帐号准备好了哇！</h1>',
            u'<p>请尽快使用下面的验证码来完成注册：</p>'
            u'<p style="font-size:36px;">{{captcha}}</p>'
        ]),
    }


class RecoveryMatter(BaseMatter):

    SUBJECT = {
        'en': u'TaokeBao: Retrieve Password',
        'zh': u'淘客宝：找回密码',
    }
    TEMPLATE = {
        'en': u''.join([
            u'<h1>Reset your password!</h1>',
            u'<p>Hello {{meta.display_name}}:</p>',
            u'<p>This email is for reset your password, ',
            u'if you are not make this request, please ignore it.</p>',
            u'<p>There is the Captcha code for recovery password:</p>',
            u'<p style="font-size:36px;">{{captcha}}</p>',
            u'<p>You have {{(expires_in / 60)|int}} minutes ',
            u'to finish this operation.</p>',
            u'<hr><p>CEO: Hayangsu</p><p>&copy; Soopro Co.,Ltd.</p>',
        ]),

        'zh': u''.join([
            u'<h1>重置您的密码！</h1>',
            u'<p>您好 {{meta.display_name}}:</p>',
            u'<p>这个邮件将帮助您重置密码，如果您没有这个打算，请无视。</p>',
            u'<p>输入下面的验证码完成密码重置：</p>',
            u'<p style="font-size:36px;">{{captcha}}</p>',
            u'<p>请您在{{(expires_in / 60)|int}}分钟内完成这个操作。</p>'
        ])
    }
