import os
from io import BytesIO                                # StringIO and BytesIO are parts of io module in python3
from pathlib import Path
from django.contrib.auth.models import AnonymousUser, User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase, Client, RequestFactory
from members.models import Member
from .models import Tag, Image, Sound, Code, Link
from .utils import TestData
from .views import *

# Create your tests here.

class ImageTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.data = TestData()
        self.member, self.user = self.data.create_test_member()
        # Login
        self.client.login(username=self.user, password="testpassword")
        self.assertIn('_auth_user_id', self.client.session)

    def tearDown(self):
        f = Path(self.data.image_path)
        if f.is_file():
            f.unlink()

    def test_read_urls(self):
        # GET empty public Image list
        request = self.factory.get('/')
        request.user = self.user
        response = self.client.get(reverse('objects:public_images'))
        self.assertEqual(response.status_code, 200)
        # GET Member Image list
        request = self.factory.get('/')
        request.user = self.user
        response = self.client.get(reverse('objects:member_images', kwargs={'member': self.member.username}))
        self.assertEqual(response.status_code, 200)
        # GET create view
        request = self.factory.get('/')
        request.user = self.user
        response = self.client.get(reverse('objects:image_create'))
        self.assertEqual(response.status_code, 200)

    def test_post_create(self):
        # POST create view
        request = self.factory.get('/')
        request.user = self.user
        data, img = self.data.small_image(self.member)
        response = self.client.post(
            reverse('objects:image_create'),
            data,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
 
    def test_post_update(self):
        # POST update view
        request = self.factory.get('/')
        request.user = self.user
        data, img = self.data.small_image(self.member)
        response = self.client.post(
            reverse(
                'objects:image_update',
                kwargs={'pk': Image.objects.all()[0].pk}
            ),
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
        
class SoundTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.data = TestData()
        self.client = Client()
        self.member, self.user = self.data.create_test_member()
        self.user = User.objects.get(pk=self.member.pk)
        # Login
        self.client.login(username=self.user, password="testpassword")
        self.assertIn('_auth_user_id', self.client.session)

    def tearDown(self):
        f = Path(self.data.sound_path)
        if f.is_file():
            f.unlink()

    def test_read_urls(self):
        request = self.factory.get('/')
        request.user = self.user
        # GET empty public Sound list
        response = self.client.get(reverse('objects:public_sounds'))
        self.assertEqual(response.status_code, 200)
        # GET Member Sound list
        response = self.client.get(reverse('objects:member_sounds', kwargs={'member': self.member.username}))
        self.assertEqual(response.status_code, 200)
        # GET create view
        response = self.client.get(reverse('objects:sound_create'))
        self.assertEqual(response.status_code, 200)

    def test_create_urls(self):
        # POST create view
        request = self.factory.get('/')
        request.user = self.user
        data, smp = self.data.small_sound(self.member)
        response = self.client.post(
            reverse('objects:sound_create'),
            data,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
 
    def test_update_urls(self):
        request = self.factory.get('/')
        request.user = self.member
        data, smp = self.data.small_sound(self.member)
        response = self.client.post(
            reverse(
                'objects:sound_update',
                kwargs={'pk': Sound.objects.all()[0].pk}
            ),
            data,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

    def test_urls_anonymously(self):
        self.client.logout()
        data, smp = self.data.small_sound(self.member)
        # GET public Sound list
        response = self.client.get(reverse('objects:public_sounds'))
        self.assertEqual(response.status_code, 302)
        # GET Member Sound list
        response = self.client.get(
            reverse(
                'objects:member_sounds',
                kwargs={'member': self.member.username}
            )
        )
        self.assertEqual(response.status_code, 302)
        # GET create view
        response = self.client.get(reverse('objects:sound_create'))
        self.assertEqual(response.status_code, 302)
        # GET detail view
        response = self.client.get(
            reverse(
                'objects:sound_detail',
                kwargs={'pk': Sound.objects.all()[0].pk}
            )
        )
        self.assertEqual(response.status_code, 302)
        
class CodeTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.data = TestData()
        self.member, self.user = self.data.create_test_member()
        # Login
        self.client.login(username=self.user, password=self.data.password)
        self.assertIn('_auth_user_id', self.client.session)

    def tearDown(self):
        pass

    def test_read_urls(self):
        request = self.factory.get('/')
        request.user = self.user
        # GET empty public Code list
        response = self.client.get(reverse('objects:public_code'))
        self.assertEqual(response.status_code, 200)
        # GET Member Code list
        response = self.client.get(reverse('objects:member_code', kwargs={'member': self.member.username}))
        self.assertEqual(response.status_code, 200)
        # GET create view
        response = self.client.get(reverse('objects:code_create'))
        self.assertEqual(response.status_code, 200)

    def test_post_create(self):
        # POST create view
        request = self.factory.get('/')
        request.user = self.user
        data = self.data.link_data()
        response = self.client.post(
            reverse('objects:code_create'),
            data,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
 
    def test_post_update(self):
        request = self.factory.get('/')
        request.user = self.user
        # POST update view
        data = self.data.code_data()
        code = Code.objects.create(owner=self.member, **data)
        code.save()
        # POST create view
        response = self.client.post(
            reverse('objects:code_update', kwargs={'pk': code.pk}),
            data,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

    def test_urls_anonymously(self):
        data = self.data.code_data()
        code = Code.objects.create(owner=self.member, **data)
        code.save()
        self.client.logout()
        # GET public Code list
        response = self.client.get(reverse('objects:public_code'))
        self.assertEqual(response.status_code, 302)
        # GET Member Code list
        response = self.client.get(
            reverse(
                'objects:member_code',
                kwargs={'member': self.member.username}
            )
        )
        self.assertEqual(response.status_code, 302)
        # GET create view
        response = self.client.get(reverse('objects:code_create'))
        self.assertEqual(response.status_code, 302)
        # GET detail view
        response = self.client.get(
            reverse(
                'objects:code_detail',
                kwargs={'pk': code.pk}
            )
        )
        self.assertEqual(response.status_code, 302)
        
class LinkTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.client = Client()
        self.data = TestData()
        self.member, self.user = self.data.create_test_member()
        # Login
        self.client.login(username=self.user, password=self.data.password)
        self.assertIn('_auth_user_id', self.client.session)
        # Create an Image
        data, img = self.data.small_image(self.member)

    def tearDown(self):
        f = Path(self.data.image_path)
        if f.is_file():
            f.unlink()

    def test_read_urls(self):
        request = self.factory.get('/')
        request.user = self.user
        # GET empty public Link list
        response = self.client.get(reverse('objects:public_links'))
        self.assertEqual(response.status_code, 200)
        # GET Member Link list
        response = self.client.get(reverse('objects:member_links', kwargs={'member': self.member.username}))
        self.assertEqual(response.status_code, 200)
        # GET create view
        response = self.client.get(reverse('objects:link_create'))
        self.assertEqual(response.status_code, 200)

    def test_post_create(self):
        # POST create view
        request = self.factory.get('/')
        request.user = self.user
        data = self.data.link_data()
        response = self.client.post(
            reverse('objects:link_create'),
            data,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
 
    def test_post_update(self):
        request = self.factory.get('/')
        request.user = self.user
        # POST update view
        data = self.data.link_data()
        link = Link.objects.create(owner=self.member, **data)
        link.save()
        # POST create view
        response = self.client.post(
            reverse('objects:link_update', kwargs={'pk': link.pk}),
            data,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

    def test_urls_anonymously(self):
        # Create Image
        data = self.data.link_data()
        link = Link.objects.create(owner=self.member, **data)
        link.save()
        # Logout the member
        self.client.logout()
        # GET public Link list
        response = self.client.get(reverse('objects:public_links'))
        self.assertEqual(response.status_code, 302)
        # GET Member Link list
        response = self.client.get(
            reverse(
                'objects:member_links',
                kwargs={'member': self.member.username}
            )
        )
        self.assertEqual(response.status_code, 302)
        # GET create view
        response = self.client.get(reverse('objects:link_create'))
        self.assertEqual(response.status_code, 302)
        # GET detail view
        response = self.client.get(
            reverse(
                'objects:link_detail',
                kwargs={'pk': link.pk}
            )
        )
        self.assertEqual(response.status_code, 302)
        
