"""
Tests for email functionality in pytest style.
Command to run tests:
    - pytest -v -s companies\tests\test_emails_pt.py --durations=0
"""

from django.core import mail

from rest_framework import status

from unittest.mock import patch, MagicMock

from smtplib import SMTPException

import os
import json

from dotenv import load_dotenv

load_dotenv()


EMAIL_URL = '/send-email'


def test_send_email_success(settings, mailoutbox):
    settings.EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'
    assert len(mailoutbox) == 0
    mail.send_mail(
        subject='Test Subject',
        message='Some test message',
        from_email=os.environ.get('SENDER_EMAIL'),
        recipient_list=[os.environ.get('RECEIVER_EMAIL')],
        fail_silently=False
    )
    assert len(mailoutbox) == 1
    assert mailoutbox[0].subject == 'Test Subject'

def test_send_email_without_args_sends_empty_email(client):
    with patch('companies.views.send_mail') as mock_send_email_func:
        r = client.post(path=EMAIL_URL)
        r_content = json.loads(r.content)

        assert r.status_code == status.HTTP_200_OK
        assert r_content['status'] == 'success'
        assert r_content['info'] == 'email sent successfully'

        mock_send_email_func.assert_called_with(
            subject=None,
            message=None,
            from_email=os.environ.get('SENDER_EMAIL'),
            recipient_list=[os.environ.get('RECEIVER_EMAIL')]
        )

def test_send_email_with_get_method_fails(client):
    r = client.get(path=EMAIL_URL)
    assert r.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert json.loads(r.content) == {'detail': 'Method "GET" not allowed.'}


@patch('companies.views.send_mail', MagicMock(side_effect=SMTPException()))
def test_smtp_error_response(client) -> None:
    """Test response 500 when sending an email raises SMTPException."""

    # with patch('companies.views.send_mail', MagicMock(side_effect=SMTPException())):
    #     r = client.post(path=EMAIL_URL)

    r = client.post(path=EMAIL_URL)

    assert r.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert r.data['status'] == 'fail'
