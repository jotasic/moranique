
import datetime
from unittest import mock

from django.contrib.auth import get_user_model
from rest_framework      import status
from rest_framework.test import APITestCase

from .models import Post, Category


class BlogPostTestCase(APITestCase):
    maxDiff = None

    def setUp(self):
            self.user = get_user_model().objects.create_user(
                email    = 'moranique@gmail.com',
                password = '12345678',
                nickname = '모라니크',
                date_of_birth = '2020-01-01'
            )

            self.cate_study = Category.objects.create(name='공부')
            self.cate_hobby = Category.objects.create(name='취미')

            self.mocked_date_time = datetime.datetime(2021,1,1,0,0,0)

            with mock.patch('django.utils.timezone.now', mock.Mock(return_value=self.mocked_date_time)):
                self.post_today_hooby = Post.objects.create(
                    author      = self.user,
                    title     = '오늘의 취미 활동',
                    content   = '오늘은 등산을 하였습니다.',
                    category = self.cate_hobby
                )

                self.post_today_study =Post.objects.create(
                    author      = self.user,
                    title     = '스터디 활동',
                    content   = '오늘은 팀원들과 만나서 Python에 대해서 공부하였습니다.',
                    category = self.cate_study
                )
    
    def test_get_post_list(self):
        response = self.client.get('/api/blogs')
        expected_data = [
        {
            "id": self.post_today_study.id,
            "category": {
                "id": self.cate_study.id,
                "name": "공부"
            },
            "author": {
                "id": self.user.id,
                "nickname": "모라니크",
                "email": "moranique@gmail.com",
            },
            "tags": [],
            "files": [],
            "title": "스터디 활동",
            "content": "오늘은 팀원들과 만나서 Python에 대해서 공부하였습니다.",
            "created_at": self.mocked_date_time.strftime('%Y-%m-%dT%H:%M:%S'),
            "edited_at": self.mocked_date_time.strftime('%Y-%m-%dT%H:%M:%S'),
            "is_active": True
        },
        {
            "id": self.post_today_hooby.id,
            "category": {
                "id": self.cate_hobby.id,
                "name": "취미"
            },
            "author": {
                "id": self.user.id,
                "nickname": "모라니크",
                "email": "moranique@gmail.com",
            },
            "tags": [],
            "files": [],
            "title": "오늘의 취미 활동",
            "content": "오늘은 등산을 하였습니다.",
            "created_at": self.mocked_date_time.strftime('%Y-%m-%dT%H:%M:%S'),
            "edited_at": self.mocked_date_time.strftime('%Y-%m-%dT%H:%M:%S'),
            "is_active": True
        }]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_data)

    def test_get_post_list_using_title_filter(self):
        response = self.client.get('/api/blogs?title=스터디')
        expected_data = [
        {
            "id": self.post_today_study.id,
            "category": {
                "id": self.cate_study.id,
                "name": "공부"
            },
            "author": {
                "id": self.user.id,
                "nickname": "모라니크",
                "email": "moranique@gmail.com",
            },
            "tags": [],
            "files": [],
            "title": "스터디 활동",
            "content": "오늘은 팀원들과 만나서 Python에 대해서 공부하였습니다.",
            "created_at": self.mocked_date_time.strftime('%Y-%m-%dT%H:%M:%S'),
            "edited_at": self.mocked_date_time.strftime('%Y-%m-%dT%H:%M:%S'),
            "is_active": True
        }]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expected_data)


    def test_get_post_list_using_category_filter(self):
        response = self.client.get('/api/blogs?category=공부')
        expected_data = [
        {
            "id": self.post_today_study.id,
            "category": {
                "id": self.cate_study.id,
                "name": "공부"
            },
            "author": {
                "id": self.user.id,
                "nickname": "모라니크",
                "email": "moranique@gmail.com",
            },
            "tags": [],
            "files": [],
            "title": "스터디 활동",
            "content": "오늘은 팀원들과 만나서 Python에 대해서 공부하였습니다.",
            "created_at": self.mocked_date_time.strftime('%Y-%m-%dT%H:%M:%S'),
            "edited_at": self.mocked_date_time.strftime('%Y-%m-%dT%H:%M:%S'),
            "is_active": True
        }]

    def test_create_blog_post_no_token(self):
        data = {
            'title'     : '오늘의 영화',
            'content'   : '오늘의 영화는 코미디 입니다!',
            'category'  : self.cate_hobby.id,
            'tags'      : '["영화","코미디"]'
        }
        response = self.client.post('/api/blog/create', data=data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_blog_post(self):
        self.client.force_authenticate(self.user)
        data = {
            'title'     : '오늘의 영화',
            'content'   : '오늘의 영화는 코미디 입니다!',
            'category'  : self.cate_hobby.id,
            'tags'      : '["일상", "공유"]',
        }
        response = self.client.post('/api/blog/create', data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_blog_post_without_tags(self):
        self.client.force_authenticate(self.user)
        data = {
            'title'     : '오늘의 영화',
            'content'   : '오늘의 영화는 코미디 입니다!',
            'category'  : self.cate_hobby.id,
            'tags' : "[]"
        }
        response = self.client.post('/api/blog/create', data=data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)