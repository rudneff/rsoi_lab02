from django.contrib import admin

from django.utils.translation import ugettext_lazy as _
from ask_api.forms import CustomUserChangeForm, CustomUserCreateForm
from ask_api.models import Question, Answer, CustomUser, Client
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreateForm

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('email', 'phone_number')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Activity'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone', 'password1', 'password2'),
        }),
    )

    ordering = ('username',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register([Question, Answer])
admin.site.register(Client)
