"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from django_hello_world.hello.models import UserProfile, WebRequest


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class HttpTest(TestCase):
    def setUp(self):
        User.objects.create(
            first_name='Olexandr',
            last_name='Poplavskyi',
            email=u'stu.shurik@gmail.com',
        )

        UserProfile.objects.create(
            user=User.objects.get(email='stu.shurik@gmail.com'),
            birthday='1992-06-19',
            bio='student of the CSTU',
            contacts='Chernigiv, Dotsenko str. 12 app. 17',
            jabber='stushurik@khavr.com',
            skype='shurik.poplavskyi',
            other='-'
        )

    def test_home(self):
        admin = User.objects.get(email='stu.shurik@gmail.com')
        profile = UserProfile.objects.get(user=admin)

        c = Client()
        response = c.get(reverse('home'))
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
        self.assertEqual("student of the CSTU", profile.bio)

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


class WebRequestMiddlewareTest(TestCase):

    def test_requests(self):
        c = Client()
        c.get(reverse('home'),
              PATH=reverse('home'),
              HTTP_USER_AGENT='Mozilla/5.0'
              )
        request = WebRequest.objects.filter(path=reverse('home'),
                                         user_agent='Mozilla/5.0',
                                         method='GET'
        )
        self.assertEqual(len(request),1)
