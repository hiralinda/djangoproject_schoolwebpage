from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile

class CustomUserAdmin(UserAdmin):
    # fieldsets = UserAdmin.fieldsets + (
    #     (None, {'fields': ('user_type')}),
    # )
    # add_fieldsets = UserAdmin.add_fieldsets + (
    #     (None, {'fields': ('user_type')}),
    # )

    model = CustomUser

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)
