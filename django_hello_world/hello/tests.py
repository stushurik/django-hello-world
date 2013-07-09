"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from StringIO import StringIO
import json
import sys

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.test import TestCase

from django_hello_world.hello.models import WebRequest, ModelsOperation
from django_hello_world.hello.templatetags.extended_tags import edit_link


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
        response = self.client.post(reverse('requests_list'), {'start': "0", 'end': "0"})
        self.assertTemplateUsed(response, 'hello/request_list.html')
        response = self.client.post(reverse('requests_list'), {'start': "string", 'end': "string"})
        self.assertContains(response, 'Please enter integer value of priority!')

        response_data_v1 = {'success': True,
                            'message': "Priority was successful changed!"
                            }
        response_data_v2 = {'success': False,
                            'message': "Error: with DB operations!"
                            }
        response_data_v3 = {'success': False,
                            'message': "Error: priority value is not integer!"
                            }
        response_data_v4 = {'success': False,
                            'message': "Error: there is no request id!"
                            }
        response = self.client.post(reverse('change_priority'), {'id': "1", 'value': "100"})
        self.assertContains(response, json.dumps(response_data_v1))
        response = self.client.post(reverse('change_priority'), {'id': "-1", 'value': "100"})
        self.assertContains(response, json.dumps(response_data_v2))
        response = self.client.post(reverse('change_priority'), {'id': "1", 'value': "string"})
        self.assertContains(response, json.dumps(response_data_v3))
        response = self.client.post(reverse('change_priority'), {'value': "100"})
        self.assertContains(response, json.dumps(response_data_v4))

        response = self.client.post(reverse('sort'),
                                    {'id': "time",
                                     'type': "asc",
                                     'start': '0',
                                     'end': '0'
                                     }
                                    )

        request_list = WebRequest.objects.filter(priority__range=(0, 0)).order_by("-time")
        for request in request_list:
            self.assertContains(response, request.time)

    def test_login(self):
        response = self.client.post(reverse('confirm'), {'username': "admin", 'pass': "2"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        response = self.client.post(reverse('confirm'), {'username': "admin", 'pass': "admin"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        self.client.logout()

    def test_redirect(self):
        response = self.client.get(reverse('profile'))
        self.assertRedirects(response, reverse('login'))
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)

    def test_hello_message(self):
        self.client.login(username="admin", password="admin")
        response = self.client.get(reverse('home'))
        self.assertContains(response, "Hello, <strong>admin</strong> !")
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_logout_link(self):
        self.client.login(username="admin", password="admin")
        response = self.client.get(reverse('profile'))
        self.assertContains(response, "Logout")

    def test_edit_page_content(self):
        self.client.login(username="admin", password="admin")
        response = self.client.get(reverse('profile'))
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

    def test_data_edit_view(self):
        response_data = {'success': False,
                         'message': "Error while saving data!"
                         }
        response = self.client.post(reverse('save_profile'), {'foo': 'bar'})
        self.assertContains(response, json.dumps(response_data))
        admin = User.objects.get(username='admin')
        self.client.login(username="admin", password="admin")
        self.client.post(reverse('save_profile'),
                         {'first_name': 'Test',
                          'last_name': 'Test',
                          'email': 'test@test.com',
                          'birthday': '2092-12-12',
                          'bio': 'test',
                          'other': 'test',
                          'skype': 'test',
                          'jabber': 'test',
                          'contacts': 'test',
                          }
                         )

        self.assertEqual(1, len(User.objects.filter(first_name='Test',
                                                    last_name='Test',
                                                    email='test@test.com'
                                                    )
                                )
                         )
        test_user = User.objects.get(first_name='Test',
                                     last_name='Test',
                                     email='test@test.com'
                                     )
        self.assertEqual(admin.id, test_user.id)


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
        params = {"start": "0", "end": "0"}
        response = self.client.post(reverse('requests_list'), params)
        for request in request_list:
            self.assertContains(response, request.time)
            self.assertEqual(request.method, 'GET')
            self.assertEqual(request.path, reverse('home'))

        #Last 20 request not in rendered page
        request_list = WebRequest.objects.all()[10:20]
        response = self.client.post(reverse('requests_list'), params)
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


class ContextTestCase(TestCase):
    def test_index(self):
        response = self.client.get(reverse('home'))
        self.assertTrue('settings' in response.context)
        self.assertEqual(response.context['settings'], settings)


class TemplateTagTest(TestCase):
    def test_tag(self):
        admin = User.objects.get(pk=1)
        link = edit_link(admin)
        self.assertEqual(link,"/admin/auth/user/1/")


class ManagementCommandTestCase(TestCase):
    def test_command(self):
        for i in range(0, 2):
            self.client.get(reverse('home'))
            User.objects.create(username=i)
        stdout, stderr = sys.stdout, sys.stderr
        sys.stdout = c1 = StringIO()
        sys.stderr = c2 = StringIO()
        call_command('count_objects')
        self.assertTrue ('django_hello_world.hello.models.WebRequest\t2' in c1.getvalue())
        self.assertTrue ('error:django_hello_world.hello.models.WebRequest\t2' in c2.getvalue())
        self.assertTrue ('django.contrib.auth.models.User\t3' in c1.getvalue())
        self.assertTrue ('error:django.contrib.auth.models.User\t3' in c2.getvalue())
        sys.stdout, sys.stderr = stdout, stderr


class SignalProcessorTestCase(TestCase):
    def test_signal(self):
        number_of_operation = len(ModelsOperation.objects.filter(operation='Creation',
                                                                 model_class='User'
                                                                 )
                                  )
        user = User.objects.create(username='test_signal')
        self.assertEqual(number_of_operation + 1,
                         len(ModelsOperation.objects.filter(operation='Creation',
                                                            model_class='User'
                                                            )
                             )
                         )
        number_of_operation = len(ModelsOperation.objects.filter(operation='Editing',
                                                                 model_class='User'
                                                                 )
                                  )
        user.username = 'test_signal_edit'
        user.save()
        self.assertEqual(number_of_operation + 1,
                         len(ModelsOperation.objects.filter(operation='Editing',
                                                            model_class='User'
                                                            )
                             )
                         )
        number_of_operation = len(ModelsOperation.objects.filter(operation='Deletion',
                                                                 model_class='User'
                                                                 )
                                  )
        user.delete()
        self.assertEqual(number_of_operation + 1,
                         len(ModelsOperation.objects.filter(operation='Deletion',
                                                            model_class='User'
                                                            )
                             )
                         )
