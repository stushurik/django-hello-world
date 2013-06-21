"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from django_hello_world.hello.models import UserProfile


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class HttpTest(TestCase):
    def test_home(self):

        c = Client()
        response = c.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Name')
        self.assertContains(response,"Olexandr")

        self.assertContains(response, 'Last name')
        self.assertContains(response,"Poplavskyi")

        self.assertContains(response, 'Date of birth')
        self.assertContains(response,"19.06.92")

        self.assertContains(response, 'Bio')
        self.assertContains(response,"student of the CSTU")

        self.assertContains(response, 'Email')
        self.assertContains(response,"stu.shurik@gmail.com")

        self.assertContains(response, 'Contacts')
        self.assertContains(response,"Chernigiv, Dotsenko str. 12 app. 17")

        self.assertContains(response, 'Jabber')
        self.assertContains(response, "stushurik@khavr.com")

        self.assertContains(response, 'Skype')
        self.assertContains(response,"shurik.poplavskyi")

        self.assertContains(response, 'Other contacts')
        self.assertContains(response,"-")
