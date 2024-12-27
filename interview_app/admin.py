from django.contrib import admin

from .models import Company


# Register your models here.

class CompanyAdmin(admin.ModelAdmin):
    fieldsets = [
        ("company_name", {"fields": ['company_name', 'description', 'number_of_employees', 'owner']}),
    ]
    search_fields = ['company_name',]

admin.site.register(Company, CompanyAdmin)
