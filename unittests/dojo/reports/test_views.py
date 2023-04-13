import django
django.setup()

import unittest
from django.test import RequestFactory
from dojo.reports.views import down
from django.contrib.auth.models import User

class TestDownView(unittest.TestCase):
    
    def setUp(self):
        self.factory = RequestFactory()
    
    def test_down_view(self):
        request = self.factory.get('/dojo/reports/views/down/')
        username = 'testuser'
        user, created = User.objects.get_or_create(username=username)
        request.user = user
        response = down(request)
        self.assertEqual(response.status_code, 200)
        # Add more assertions as necessary

