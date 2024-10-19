from rest_framework import status

from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

from django.core.mail import send_mail

from companies.models import Company
from companies.serializers import CompanySerializer

import os
from dotenv import load_dotenv
from smtplib import SMTPException

load_dotenv()


class CompanyViewSet(ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all().order_by('-last_updated')
    pagination_class = PageNumberPagination


@api_view(http_method_names=['POST'])
def send_company_email(request: Request) -> Response:
    """Sends an email with request payload"""

    try:
        send_mail(
            subject=request.data.get('subject'),
            message=request.data.get('message'),
            from_email=os.environ.get('SENDER_EMAIL'),
            recipient_list=[os.environ.get('RECEIVER_EMAIL')],
        )
        payload = {'status': 'success', 'info': 'email sent successfully'}
    except (SMTPException, Exception) as e:
        payload = {'status': 'fail', 'info': str(e)}
    finally:
        return Response(payload)
