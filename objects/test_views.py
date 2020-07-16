import os
from io import BytesIO                                # StringIO and BytesIO are parts of io module in python3
from pathlib import Path
from django.contrib.auth.models import AnonymousUser, User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase, Client, RequestFactory
from django.test.utils import setup_test_environment
from members.models import Member
from .models import Tag, Image, Sound, Code, Link
from .utils import TestData
from .views import *


class ImageTest(TestCase):

    def setUp(self):
        self.data = TestData()
        self.client = Client()
        # Create a memeber
        self.member, self.user = self.data.create_test_member()
        # Login

    def tearDown(self):
        pass

    # Test Create views
    def test_create_views(self):
        response = self.client.post(reverse('objects:image_create'))
    # Test Read views
    # Test Update views
    # Test Delete views
    # Test context
    # Test publish views
    
