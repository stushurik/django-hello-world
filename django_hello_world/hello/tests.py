"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import json
from django.conf import settings
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse
from django.test import TestCase
from django_hello_world.hello.models import UserProfile, WebRequest, ModelsOperation


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class HttpTest(TestCase):
    def test_home(self):
        admin = User.objects.get(email='stu.shurik@gmail.com')
        profile = UserProfile.objects.get(user=admin)

        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Name')
        self.assertContains(response, admin.first_name)
        self.assertEqual("Olexandr", admin.first_name)

        self.assertContains(response, 'Last name')
        self.assertContains(response, admin.last_name)
        self.assertEqual("Poplavskyi", admin.last_name)

        self.assertContains(response, 'Date of birth')
        self.assertContains(response, profile.birthday)
        self.assertEqual("1992-06-19", str(profile.birthday))

        self.assertContains(response, 'Bio')
        self.assertContains(response, profile.bio)
        self.assertEqual('student of the CSTU', profile.bio)

        self.assertContains(response, 'Email')
        self.assertContains(response, admin.email)
        self.assertEqual("stu.shurik@gmail.com", admin.email)

        self.assertContains(response, 'Contacts')
        self.assertContains(response, profile.contacts)
        self.assertEqual("Chernigiv, Dotsenko str. 12 app. 17", profile.contacts)

        self.assertContains(response, 'Jabber')
        self.assertContains(response, profile.jabber)
        self.assertEqual("stushurik@khavr.com", profile.jabber)

        self.assertContains(response, 'Skype')
        self.assertContains(response, profile.skype)
        self.assertEqual("shurik.poplavskyi", profile.skype)

        self.assertContains(response, 'Other contacts')
        self.assertContains(response, profile.other)
        self.assertEqual("-", profile.other)

    def test_requests(self):
        response = self.client.get(reverse('requests'))
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        response = self.client.post(reverse('profile'), {'username': "admin", 'pass': "2"})
        self.assertRedirects(response, reverse('login'))
        response = self.client.post(reverse('profile'), {'username': "admin", 'pass': "1"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Olexandr")
        self.assertContains(response, "Poplavskyi")
        self.assertContains(response, "1992-06-19")
        self.assertContains(response, "stu.shurik@gmail.com")
        self.assertContains(response, "Chernigiv, Dotsenko str. 12 app. 17")
        self.assertContains(response, "student of the CSTU")
        self.assertContains(response, "stushurik@khavr.com")
        self.assertContains(response, "shurik.poplavskyi")
        self.assertContains(response, "-")

    def test_save(self):
        response_data = {'success': False,
                         'message': "Error while saving data!"
                         }
        response = self.client.post(reverse('save_profile'), {'foo': 'bar'})
        self.assertContains(response, json.dumps(response_data))

    def test_admin_page(self):
        self.client.login(username='admin', password='1')
        response = self.client.get('/admin/auth/user/1/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/admin/auth/user/100/')
        self.assertEqual(response.status_code, 404)


class WebRequestMiddlewareTest(TestCase):

    def test_requests(self):
        self.client.get(reverse('home'),
                        PATH=reverse('home'),
                        HTTP_USER_AGENT='Mozilla/5.0'
                        )
        request = WebRequest.objects.filter(path=reverse('home'),
                                            user_agent='Mozilla/5.0',
                                            method='GET'
                                            )
        self.assertEqual(len(request), 1)


class ContextProcessorTestCase(TestCase):
    def test_index(self):
        response = self.client.get(reverse('home'))
        self.assertTrue('settings' in response.context)
        self.assertEqual(response.context['settings'], settings)
