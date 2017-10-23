# coding=utf-8
from __future__ import absolute_import

import unittest
import shutil
import os

from flask import current_app, json

from application import create_app

from utils.auth import generate_sid


# basic
class BasicTester(unittest.TestCase):
    def setUp(self):
        config_name = 'testcase'
        os.environ['JULOLO_CONFIG_NAME'] = config_name
        self.app = create_app(config_name)
        # print self.app.config.get('APPS_FOLDER')
        # if os.path.isdir(self.app.config.get('APPS_FOLDER')):
        #     print 'set up delete'
        #     shutil.rmtree(self.app.config.get('APPS_FOLDER'))

        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.mongodb_conn.drop_database(
            self.app.config.get('MONGODB_DATABASE') or 'test')
        self.test_file_folder = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), 'testfiles')

    def tearDown(self):
        self.app.mongodb_conn.drop_database(
            self.app.config.get('MONGODB_DATABASE') or 'test')

        # if os.path.isdir(self.app.config.get('APPS_FOLDER')):
        #     shutil.rmtree(self.app.config.get('APPS_FOLDER'))

        theme_folder = self.app.config.get('THEMES_FOLDER')
        if os.path.isdir(theme_folder):
            for root, dirs, files in os.walk(theme_folder):
                for d in dirs:
                    if d != 'default':
                        shutil.rmtree(os.path.join(root, d))
                for f in files:
                    os.remove(os.path.join(root, f))
                break

        self.app_context.pop()

    def assert_all_in(self, *keys, **kargs):
        container = kargs.get('container')
        for key in keys:
            self.assertIn(key, container)


# no user, no app
class APIBaseTester(BasicTester):
    def setUp(self):
        super(APIBaseTester, self).setUp()
        self.client = self.app.test_client()

        self.default_user = {
            'log': 'testuser@test.com',
            'pwd': '123456',
            'pwd2': '123456',
            'slug': 'test_user'
        }

        self.default_email = {
            'log': self.default_user['log'],
            'meta': {'test': 'test'},
            'template': 'test template',
            'subject': 'test subject'
        }

        self.default_app = {
            'slug': 'test_app',
            'type': 'ws',
            'title': 'test_app_title',
            'local': 'en',
            'description': 'test_app_description'
        }

    @staticmethod
    def parse_response(resp):
        return json.loads(resp)

    def parse_content(self, data):
        decoded = self.parse_response(data)
        return decoded

    def parse_err_code(self, data):
        decoded = self.parse_response(data)
        return decoded['errcode']

    @property
    def default_header(self):
        return [('Content-Type', 'application/json')]

    @property
    def headers(self):
        default_headers = self.default_header
        default_headers.append(('Authorization', 'Bearer {}'.format(
            self.default_user['token'])))
        return default_headers

    @property
    def upload_headers(self):
        headers = [('Content-Type', 'multipart/form-data'),
                   ('Authorization', 'Bearer {}'.format(
                       self.default_user['token']))]
        return headers

    def user_register(self):
        headers = self.default_header
        data = {
            'log': self.default_user['log'],
            'meta': self.default_email['meta'],
            'template': self.default_email['template'],
            'code': None,
            'subject': self.default_email['subject'],
        }
        api = '/user/register'
        response = self.client.post(api, headers=headers,
                                    data=json.dumps(data))
        # print response.data
        self.assertEqual(response.status_code, 200)
        content = self.parse_content(response.data)
        self.default_user['id'] = content['id']

    def user_activate(self):
        self.user_register()

        uid = self.default_user['id']
        sid = generate_sid(uid)

        headers = self.default_header
        api = '/user/activate'
        data = {
            'sid': sid,
            'pwd': self.default_user['pwd'],
            'pwd2': self.default_user['pwd2'],
            'slug': self.default_user['slug'],
            'plan': 0,
        }
        response = self.client.post(api, headers=headers,
                                    data=json.dumps(data))
        # print response.data
        self.assertEqual(response.status_code, 200)

    def user_login(self):
        self.user_activate()

        headers = self.default_header
        api = '/user/login'
        data = {
            'log': self.default_user['log'],
            'pwd': self.default_user['pwd'],
        }
        response = self.client.post(api, data=json.dumps(data),
                                    headers=headers)
        self.assertEqual(response.status_code, 200)
        content = self.parse_content(response.data)
        self.default_user['token'] = content['token']
        self.default_user['id'] = content['id']

    def create_app(self, type='ws'):
        self.default_app['type'] = type

        headers = self.headers
        api = '/app'
        data = self.default_app
        response = self.client.post(api, data=json.dumps(data),
                                    headers=headers)
        self.assertEqual(response.status_code, 200)
        # print response.data
        content = self.parse_content(response.data)
        self.default_app['id'] = content['id']
        self.default_app['slug'] = data['slug']

    # def test_user_base(self):
    #     print '*********************'
    #     print 'user login:'
    #     print self.user_login()
    #     print '*********************'
    #     print 'create app:'
    #     print self.create_app()
    #     print '*********************'


# default user
class APITester(APIBaseTester):
    def setUp(self):
        super(APITester, self).setUp()
        self.user_login()


# default app
class AppBaseTester(APITester):
    def setUp(self):
        super(AppBaseTester, self).setUp()
        self.create_app()


class ExtDevBaseTester(AppBaseTester):
    def setUp(self):
        super(ExtDevBaseTester, self).setUp()
        self.create_extension()
        self.default_custom_extension = {
            'author': 'soopro_test',
            'title': 'test_extension',
            'description': 'Soopro test extension',
            'type': 'ws',
            'capability': 0,
            'protocol': 'http',
            'domain': '',
            'path': '/test/',
            'thumbnail': 'test.png',
            'previews': ['test_preview.png']
        }

    def tearDown(self):
        self.default_extension.delete()
        super(ExtDevBaseTester, self).tearDown()

    def create_extension(self):
        extension = current_app.mongodb.Extension()
        extension['slug'] = u'extensionfortest'
        extension['payload']['meta'] = {
            'title': u'title',
            'thumbnail': u'thumbnail_url',
            'previews': [u'preview'],
            'type': 'ws',
            'capability': 0,
            'description': u'datdescription'
        }
        extension.save()

        customer = current_app.mongodb.Customer.find_one_by_uid(
            self.default_user['id'])
        customer.extensions.append(extension['_id'])
        customer.save()

        self.default_extension = extension
