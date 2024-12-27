from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from .views import CreateCompanyView, GetCompaniesView, GetOrUpdateSingleCompanyView

urlpatterns = [
    path('companies/create', CreateCompanyView.as_view(), name='create-company'),
    path('companies/<pk>', GetOrUpdateSingleCompanyView.as_view(), name='single-company'),
    path('companies/', GetCompaniesView.as_view(), name='all-companies'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]