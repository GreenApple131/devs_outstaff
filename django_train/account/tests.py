from django.test import TestCase
from django.contrib.auth.models import User
# Create your tests here.


class UserTestCase(TestCase):
    def test_user(self):
        username = 'testcase'
        password = 'hellopass'
        u = User(username=username)
        u.save_password(password)
        u.save()
        self.assertEqual(u.username, username)
        self.assertTrue(u.check_password(password))
