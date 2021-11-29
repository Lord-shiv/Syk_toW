from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, UserManager, Profile
from . forms import UserAdminCreationForm, UserAdminChangeForm


class UserAdmin(BaseUserAdmin):
    ''' The forms to add and change user instances '''
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    date_hierarchy = 'date_joined'

    list_display = ('email', 'username', 'is_admin', 'is_staff', 'is_active', 'date_joined', 'last_login',)
    readonly_fields = ('id', 'date_joined', 'last_login')
    list_filter = ('username', 'is_staff', 'is_admin', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password',)
            }),
        ('Personal info', {
            'fields': ('username',)
            }),
        ('Permissions', {
            'fields': ('is_staff', 'is_active',)
            }),
        ('Group Permissions', {
            'classes': ('collapse',),
            'fields': ('groups', 'user_permissions',)
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    search_fields = ('username', 'email',)
    ordering = ('email',)
    filter_horizontal = ()

    def has_add_permission(self, request, obj=None):
        return True
        # request.user.is_admin

    # def has_delete_permission(self, request, obj=None):
    #     if request.user.groups.filter(name='staff').exists():
    #         # staff can't delete users
    #         return False
    #     return obj

    def has_change_permission(self, request, obj=None):
        if request.user.groups.filter(name='staff').exists():
            # staff can't delete users
            return False
        return True


admin.site.register(User, UserAdmin)
admin.site.register(Profile)
