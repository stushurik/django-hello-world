"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.conf import settings
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse
from django.test import TestCase
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


class ContextTestCase(TestCase):
    def test_index(self):
        response = self.client.get(reverse('home'))
        self.assertTrue('settings' in response.context)
        self.assertEqual(response.context['settings'], settings)
