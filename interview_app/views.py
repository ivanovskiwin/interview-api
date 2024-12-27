from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.filters import OrderingFilter
from django.core.mail import send_mail
from django.conf import settings
from .serializers import CompaniesSerializer, CompanySerializer
from .models import Company
from .pagination import MyPagination

class GetCompaniesView(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompaniesSerializer
    pagination_class = MyPagination
    filter_backends = (OrderingFilter,)
    http_method_names=['get']

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        return super().get_queryset(*args, **kwargs).filter(owner=user)
        

class GetOrUpdateSingleCompanyView(generics.RetrieveUpdateAPIView):
    queryset=Company.objects.all()
    serializer_class=CompanySerializer
    http_method_names = ['get', 'patch']

    def patch(self, request, pk):
        user = request.user
        number_of_employees = request.data.get('number_of_employees')
        if number_of_employees:
            try:
                company = Company.objects.filter(id=pk, owner=user).update(number_of_employees=number_of_employees)
                if company:
                    updated_company = Company.objects.filter(id=pk)
                    serializer = CompanySerializer(updated_company[0], many=False)
                    return Response(serializer.data, status=status.HTTP_200_OK)

                return Response({"error": "Failed to update."}, status=status.HTTP_404_NOT_FOUND)
            except:
                return Response({"error": "number_of_employees is required int field."}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"error": "number_of_employees is required int field."}, status=status.HTTP_400_BAD_REQUEST)


class CreateCompanyView(generics.CreateAPIView):
    serializer_class=CompanySerializer
    http_method_names = ['post']

    def get_queryset(self):
        user = self.request.user
        return Company.objects.filter(owner=user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(owner=self.request.user)
        else:
            return Response({"error": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
    def create(self, request, *args, **kwargs):
        user_email = request.user.email
        owned_companies = self.get_queryset().count()
        if owned_companies >= 5:
            return Response({"error": "You cannot create more than 5 companies."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            try:
                # comment this if you have problem with setting up the mail, I had a problems with the connection.
                send_mail("Company Created", "You have succesfully created a company.", settings.EMAIL_HOST_USER, [user_email])
                
                self.perform_create(serializer)
            except:
                return Response("Error sending email", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        