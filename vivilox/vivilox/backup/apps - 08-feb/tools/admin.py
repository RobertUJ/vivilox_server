#encoding:utf-8
from django.contrib import admin
from vivilox.apps.tools.models import country,province,tax,sale_percentage

admin.site.register(country)
admin.site.register(province)
admin.site.register(tax)
admin.site.register(sale_percentage)