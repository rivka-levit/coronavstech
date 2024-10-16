from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination

from companies.models import Company
from companies.serializers import CompanySerializer


class CompanyViewSet(ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all().order_by('-last_updated')
    pagination_class = PageNumberPagination
