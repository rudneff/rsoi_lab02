import datetime
from django.contrib.auth.models import User, AbstractUser, UserManager
from django.core.validators import RegexValidator
from django.db import models


class CustomUser(AbstractUser):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format:"
                                         "'+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=12, blank=True)  # validators should be a list
    REQUIRED_FIELDS = ['email', 'phone_number']

    object = UserManager()

    def __unicode__(self):
        return self.username


# Create your models here.
class Question(models.Model):
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=200)
    author = models.ForeignKey(CustomUser, related_name='questions')
    date = models.DateTimeField(default=datetime.datetime.now, blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Answer(models.Model):
    body = models.CharField(max_length=200)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    date = models.DateTimeField(default=datetime.datetime.now, blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.body


class Client(models.Model):
    secret = models.CharField(max_length=256, blank=False, null=False)
    redirect_uri = models.URLField(max_length=256, blank=True, null=True)
    name = models.CharField(max_length=32, blank=False, null=False)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


EXPIRED_DAYS = 1


def expired_time():
    return datetime.datetime.now() + datetime.timedelta(days=EXPIRED_DAYS)


class Authorization(models.Model):
    user = models.ForeignKey(CustomUser, related_name='auth_codes')
    code = models.CharField(max_length=256, blank=False, null=False)
    expired = models.DateTimeField(default=expired_time)

    is_active = models.BooleanField(default=True)


class Access(models.Model):
    user = models.ForeignKey(CustomUser, related_name='tokens')
    token = models.CharField(max_length=256, blank=False, null=False)
    expired = models.DateTimeField(default=expired_time)
    refresh_token = models.CharField(max_length=256, blank=False, null=False)

    is_active = models.BooleanField(default=True)

