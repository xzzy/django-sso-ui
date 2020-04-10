from django.contrib import messages
from django.contrib.gis import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib.admin import register, ModelAdmin

from ssoapp import models

@admin.register(models.EmailUser)
class EmailAdmin(ModelAdmin):
    list_display = ('id', 'first_name','last_name','is_staff','is_superuser',)
    list_filter = ('is_staff','is_superuser',)
    search_fields = ('first_name','last_name','id',)

