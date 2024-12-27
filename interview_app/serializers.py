from rest_framework import serializers
from .models import Company


class CompaniesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ['company_name', 'description', 'number_of_employees']

class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = '__all__'
        extra_kwargs = {"owner": {"read_only": True}}