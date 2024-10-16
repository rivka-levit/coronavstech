from rest_framework import routers

from companies.views import CompanyViewSet

companies_router = routers.DefaultRouter()
companies_router.register(prefix='companies',
                          viewset=CompanyViewSet,
                          basename='companies')
