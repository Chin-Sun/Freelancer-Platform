from django.contrib import admin
from django.contrib.auth import get_user_model


MyUserAdmin = get_user_model()
admin.site.register(MyUserAdmin)
