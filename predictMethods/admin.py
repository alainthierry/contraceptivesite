from django.contrib import admin

from .models import (User, UserData)

""" Register your models here """

admin.site.register(User)
admin.site.register(UserData)
