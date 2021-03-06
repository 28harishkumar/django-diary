from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import *
# Register your models here.

class MyUserAdmin(UserAdmin):
    UserAdmin.add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email', 'password1', 'password2','first_name'),
        }),
    )
    list_display = ('username','email','id','first_name','last_name','is_staff')
    search_fields = ('first_name', 'last_name', 'email','username')
    ordering = ('username',)

    UserAdmin.fieldsets = (
        (None, {'fields': ('username', 'email','password')}),
        ('Personal info', {'fields': ('first_name', 'last_name',)}),
        ('advance_info',{'fields':('confirmation_code',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('date_joined',)}),
    )

admin.site.register(User,MyUserAdmin)