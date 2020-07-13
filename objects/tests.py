import os
from io import BytesIO                                # StringIO and BytesIO are parts of io module in python3
from pathlib import Path
from django.contrib.auth.models import AnonymousUser, User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase, Client, RequestFactory
from members.models import Member
from .models import Tag, Image, Sound, Code, Link
from .views import *

# Create your tests here.

class ImageTest(TestCase):

    big_text = """Lorem ipsum dolor sit amet, consectetur adipiscing
elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur
sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt
mollit anim id est laborum."""
    small_text = "Duis aute irure dolor"
    image_path = os.path.join(settings.BASE_DIR, 'media/test.png')

    def get_small_image(self):
        '''
        Returns test data for image views and a raw image file
        '''
        # Create test image in media dir
        from PIL import Image as image
        test_image = image.new('RGB', (500, 500))
        test_image.save(self.image_path, "PNG")
        with open(self.image_path, 'rb') as f:
            img = BytesIO(b'f')
            img.name = "test.png"
            data = {
                'title': "Test Title",
                'image_file': img,
                'text': self.big_text,
                'credit': self.small_text,
            }
            return data, img

    def setUp(self):
        #self.factory = RequestFactory()
        self.client = Client()
        self.member = Member.objects.create_user(
            username='fred',
            email='fred@slaterock.com',
            password='testpassword',
            first_name='Fred',
            last_name='Flinstone',
        )
        self.user = User.objects.get(pk=self.member.pk)
        # Login
        self.client.login(username=self.user, password="testpassword")
        self.assertIn('_auth_user_id', self.client.session)

    def tearDown(self):
        f = Path(self.image_path)
        if f.is_file():
            f.unlink()

    def test_read_urls(self):
        # GET empty public Image list
        response = self.client.get(reverse('objects:public_images'))
        self.assertEqual(response.status_code, 200)
        # GET Member Image list
        response = self.client.get(reverse('objects:member_images', kwargs={'member': self.member.username}))
        self.assertEqual(response.status_code, 200)
        # GET create view
        response = self.client.get(reverse('objects:image_create'))
        self.assertEqual(response.status_code, 200)

    def test_post_create(self):
        # POST create view
        data, img = self.get_small_image()
        response = self.client.post(
            reverse('objects:image_create'),
            data,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
 
    def test_post_update(self):
        # POST update view
        data, img = self.get_small_image()
        image = Image.objects.create(
            title='Test Title',
            owner=Member.objects.get(username='fred'),
            image_file=self.image_path.split('/')[-1],
            text=self.big_text,
            credit=self.small_text,
        )
        image.save()
        # POST create view
        response = self.client.post(
            reverse('objects:image_update', kwargs={'pk': image.pk}),
            data,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

    def test_urls_anonymously(self):
        self.client.logout()
        # GET public Image list
        response = self.client.get(reverse('objects:public_images'))
        self.assertEqual(response.status_code, 302)
        # GET Member Image list
        response = self.client.get(reverse('objects:member_images', kwargs={'member': self.member.username}))
        self.assertEqual(response.status_code, 302)
        # GET create view
        response = self.client.get(reverse('objects:image_create'))
        self.assertEqual(response.status_code, 302)
        # GET detail view
        #response = self.client.get(reverse('objects:image_detail', kwargs={'pk':))
        #self.assertEqual(response.status_code, 302)
        
