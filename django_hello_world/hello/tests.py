"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import json
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from django_hello_world.hello.models import WebRequest


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class HttpTest(TestCase):
    fixtures = ['initial_data.json']

    def test_home(self):
        admin = User.objects.get(email='stu.shurik@gmail.com')

        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Name')
        self.assertContains(response, admin.first_name)
        self.assertEqual("Olexandr", admin.first_name)

        self.assertContains(response, 'Last name')
        self.assertContains(response, admin.last_name)
        self.assertEqual("Poplavskyi", admin.last_name)

        self.assertContains(response, 'Date of birth')
        self.assertContains(response, admin.userprofile.birthday)
        self.assertEqual("1992-06-19", str(admin.userprofile.birthday))

        self.assertContains(response, 'Bio')
        self.assertContains(response, admin.userprofile.bio)
        self.assertEqual('student of the CSTU', admin.userprofile.bio)

        self.assertContains(response, 'Email')
        self.assertContains(response, admin.email)
        self.assertEqual("stu.shurik@gmail.com", admin.email)

        self.assertContains(response, 'Contacts')
        self.assertContains(response, admin.userprofile.contacts)
        self.assertEqual("Chernigiv, Dotsenko str. 12 app. 17", admin.userprofile.contacts)

        self.assertContains(response, 'Jabber')
        self.assertContains(response, admin.userprofile.jabber)
        self.assertEqual("stushurik@khavr.com", admin.userprofile.jabber)

        self.assertContains(response, 'Skype')
        self.assertContains(response, admin.userprofile.skype)
        self.assertEqual("shurik.poplavskyi", admin.userprofile.skype)

        self.assertContains(response, 'Other contacts')
        self.assertContains(response, admin.userprofile.other)
        self.assertEqual("-", admin.userprofile.other)


class WebRequestMiddlewareTest(TestCase):

    def test_saving_one_request(self):
        self.client.get(reverse('home'),
              PATH=reverse('home'),
              HTTP_USER_AGENT='Mozilla/5.0'
              )
        request = WebRequest.objects.filter(path=reverse('home'),
                                            user_agent='Mozilla/5.0',
                                            method='GET'
                                            )
        self.assertEqual(len(request), 1)

    def test_only_first_ten_requests(self):
        for i in range(0, 10):
            self.client.cookies['request_number'] = i
            self.client.get(reverse('home'))
        for i in range(10, 20):
            self.client.cookies['request_number'] = i
            self.client.post(reverse('requests'), PATH=reverse('requests'))

        request_list = WebRequest.objects.all()[:10]
        response = self.client.get(reverse('requests'))
        for request in request_list:
            self.assertContains(response, request.time)
            self.assertEqual(request.method, 'GET')
            self.assertEqual(request.path, reverse('home'))

        #Last 20 request not in rendered page
        request_list = WebRequest.objects.all()[10:20]
        response = self.client.get(reverse('requests'))
        for request in request_list:
            self.assertNotContains(response, request.time)
            self.assertEqual(request.method, 'POST')
            self.assertEqual(request.path, reverse('requests'))


    def test_pass_params_get(self):
        params = {"test1": "str"}
        self.client.get(reverse('requests'),
              params,
              )
        request = WebRequest.objects.latest('time')
        self.assertEqual(request.path, reverse('requests'))
        self.assertEqual(request.get, json.dumps(params))

    def test_pass_params_post(self):
        params = {"test1": "str"}
        self.client.post('/admin/',
               params,
               HTTP_X_REQUESTED_WITH='XMLHttpRequest'
               )

        request = WebRequest.objects.latest('time')
        self.assertEqual(request.path, '/admin/')
        self.assertEqual(request.method, 'POST')
        self.assertEqual(request.is_ajax, True)
        self.assertEqual(request.post, json.dumps(params))
