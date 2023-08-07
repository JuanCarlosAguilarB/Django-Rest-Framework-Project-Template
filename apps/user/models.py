import uuid
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone

# https://testdriven.io/blog/django-custom-user-model/

# https://stackoverflow.com/questions/43915518/how-to-use-custom-password-validators-beside-the-django-auth-password-validators


class CustomPasswortValidator:
    """
    Custom validation for the password user.
    """

    def validate(value):

        # check minimun length of value
        if len(value) < 8:
            raise ValidationError(
                _('Password length must be greater than 8 character.'))

        # check if value has a letter capitalized
        if not any(char.isupper() for char in value):
            raise ValidationError(
                _('Password must contain at least one capital letter.'))

        # check if value has a digit
        if not any(char.isdigit() for char in value):
            raise ValidationError(_('Password must contain at least 1 digit.'))

        # check if value has a letter
        if not any(char.isalpha() for char in value):
            raise ValidationError(
                _('Password must contain at least 1 letter.'))

        # check if value has a  special character
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        if not any(char in special_characters for char in value):
            raise ValidationError(
                _('Password must contain at least one special character.'))


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def save(self, *args, **kwargs):
        self.beginning = self.story[0:100]
        return super().save(*args, **kwargs)

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """

        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        # validation password
        CustomPasswortValidator.validate(password)

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class Countries(models.Model):
    """
    Model by create and save a Country.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'countries'

    def __str__(self):
        return self.name


""" 
The default User model in Django uses a username to uniquely identify a user during authentication. 
If you'd rather use an email address, you'll need to create a custom User model by either subclassing
AbstractUser or AbstractBaseUser.

Options:

AbstractUser: Use this option if you are happy with the existing fields on the User model and just want to remove the username field. (it is not the case)
AbstractBaseUser: Use this option if you want to start from scratch by creating your own, completely new User model.

"""


def user_profile_path(instance, filename):
    """función asignar la ubicación de las imagenes en la carpeta correspondiente
    """
    return 'user_profile_photo/{0}/{1}'.format(instance.title, filename)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Model by create and save a user with given email and password.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    country = models.ForeignKey(
        Countries, models.DO_NOTHING, blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)
    password = models.CharField(max_length=128)
    username = models.CharField(
        unique=True, max_length=50, blank=True, null=True)
    photo = models.ImageField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)  # for delete account

    # fields that to need django auth models
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        db_table = 'user_auth'

    def __str__(self):
        return self.email

    def get_user_profile_photo(self):
        if self.photo:
            return self.photo.url
        return ''
