#!/usr/bin/env python3
"""
Module for test base class
"""
import unittest
from app import create_app
from models import db


class BaseTestCase(unittest.TestCase):
    """
    Class for Base Test case that test cases can inherit from
    """
    def setUp(self) -> None:
        """
        Set the app context and create the database
        """
        self.app = create_app('test')
        self.db = db
        self.app_context = self.app.app_context()
        self.test_client = self.app.test_client()
        self.test_firstname = 'testfirstname'
        self.test_lastname = 'testlastname'
        self.test_email = 'testemail@email.com'
        self.test_pwd = 'testpassword'
        self.url = '/v1'
        self.details = {
            'first_name': self.test_firstname,
            'last_name': self.test_lastname,
            'email': self.test_email,
            'password': self.test_pwd
        }

        self.login = {
            'email': self.test_email,
            'password': self.test_pwd
        }

        self.test_firstname_ = 'testfirstname2'
        self.test_lastname_ = 'testlastname2'
        self.test_email_ = 'testemail2@email.com'
        self.test_pwd_ = 'testpassword2'
        self.details_ = {
            'first_name': self.test_firstname_,
            'last_name': self.test_lastname_,
            'email': self.test_email_,
            'password': self.test_pwd_
        }

        self.login_ = {
            'email': self.test_email_,
            'password': self.test_pwd_
        }

        self.app_context.push()
        self.reg_resp = self.test_client.post(
            self.url + '/auth/register',
            json=self.details
        )

        self.reg_resp_ = self.test_client.post(
            self.url + '/auth/register',
            json=self.details_
        )

        self.login_resp = self.test_client.post(
            self.url + '/auth/login',
            json=self.login
        )

        self.login_resp_ = self.test_client.post(
            self.url + '/auth/login',
            json=self.login_
        )

        self.access_token = self.login_resp.get_json()['data']['access_token']
        self.auth_header = {
            'Authorization': f"Bearer {self.access_token}"
        }

        self.access_token_ = self.login_resp_.get_json()['data']['access_token']
        self.auth_header_ = {
            'Authorization': f"Bearer {self.access_token_}"
        }

    def tearDown(self) -> None:
        """
        Remove the app context and the database
        """
        self.db.drop_database()
        self.app_context.pop()
