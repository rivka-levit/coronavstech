"""
Serializers for Company app
"""

from rest_framework import serializers
from companies.models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'status', 'app_link', 'last_updated', 'notes']
        # read_only_fields = ['id']
