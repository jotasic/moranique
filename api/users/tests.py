from django.test import TestCase

import datetime
from unittest import mock

from django.contrib.auth import get_user_model
from rest_framework      import status
from rest_framework.test import APITestCase


class AccountTestCase(APITestCase):
    def setUp(self):
            get_user_model().objects.create_user(
                email    = 'taewookim@gmail.com',
                password = '12345678',
                nickname = '김태우',
                date_of_birth = '2020-01-01'
            )

    def test_registration_success(self):
        data = {
            "email" : "moranique@gmail.com",
            "password" : "12345678",
            "nickname" : "모라니크",
            "date_of_birth" : "2021-01-01"
        }

        response = self.client.post('/api/user/registration/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registration_failed_duto_duplicated_nickname(self):
        data = {
            "email" : "moranique@gmail.com",
            "password" : "12345678",
            "nickname" : "김태우",
            "date_of_birth" : "2021-01-01"
        }

        response = self.client.post('/api/user/registration/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_failed_duto_duplicated_email(self):
        data = {
            "email" : "taewookim@gmail.com",
            "password" : "12345678",
            "nickname" : "모라니크",
            "date_of_birth" : "2021-01-01"
        }

        response = self.client.post('/api/user/registration/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TokenTestCase(APITestCase):
    def setUp(self):
        get_user_model().objects.create_user(
            email    = 'taewookim@gmail.com',
            password = '12345678',
            nickname = '김태우',
            date_of_birth = '2020-01-01')

    
    def test_get_tocken_success(self):
        data = {
            "email" : "taewookim@gmail.com",
            "password" : "12345678"
        }

        response = self.client.post('/api/user/token/', data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_refresh_token_success(self):
        data = {
            "email" : "taewookim@gmail.com",
            "password" : "12345678"
        }
        response_new_token = self.client.post('/api/user/token/', data=data)
        self.assertEqual(response_new_token.status_code, status.HTTP_200_OK)

        data = { 'refresh' : response_new_token.json()['refresh']}
        response_refresh_token = self.client.post('/api/user/token/refresh/', data=data)
        self.assertEqual(response_refresh_token.status_code, status.HTTP_200_OK)