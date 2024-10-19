"""
Tests for email functionality in unittest style.
Command to run tests:
    - python manage.py test companies.tests.test_emails
"""

from django.test import TestCase, Client
from django.core import mail

from rest_framework import status

from unittest.mock import patch

import os
import json

from dotenv import load_dotenv

load_dotenv()


class EmailUnitTest(TestCase):
    def test_send_email_success(self):
        with self.settings(
            EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'
        ):
            self.assertEqual(len(mail.outbox), 0)
            mail.send_mail(
                subject='Test Subject',
                message='Some test message',
                from_email=os.environ.get('SENDER_EMAIL'),
                recipient_list=[os.environ.get('RECEIVER_EMAIL')],
                fail_silently=False
            )

            self.assertEqual(len(mail.outbox), 1)
            self.assertEqual(mail.outbox[0].subject, 'Test Subject')

    def test_send_email_without_args_sends_empty_email(self):
        client = Client()
        with patch('companies.views.send_mail') as mock_send_email_func:
            r = client.post(path='/send-email')
            response_content = json.loads(r.content)

            self.assertEqual(r.status_code, status.HTTP_200_OK)
            self.assertEqual(response_content['status'], 'success')
            self.assertEqual(response_content['info'], 'email sent successfully')
            mock_send_email_func.assert_called_with(
                subject=None,
                message=None,
                from_email=os.environ.get('SENDER_EMAIL'),
                recipient_list=[os.environ.get('RECEIVER_EMAIL')]
            )

    def test_send_email_with_get_method_fails(self):
        client = Client()
        r = client.get(path='/send-email')
        self.assertEqual(r.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(
            json.loads(r.content),
            {'detail': 'Method "GET" not allowed.'}
        )
