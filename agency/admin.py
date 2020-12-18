from django.contrib import admin
from .models import Agency



# Register your models here.
class AgencyAdmin(admin.ModelAdmin):
    admin.site.register(Agency)

    