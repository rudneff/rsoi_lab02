from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.forms import fields

from ask_api.models import CustomUser


class CustomUserCreateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password']


class CustomUserAuthForm(AuthenticationForm):
    state = fields.CharField(max_length=30, required=False)
    client_id = fields.IntegerField()

    class Meta:
        model = CustomUser
        fields = ['username', 'password']

