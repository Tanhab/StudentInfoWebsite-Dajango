from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

blood_group_options = [
    ('A+', 'A+'),
    ('B+', 'B+'),
    ('O+', 'O+'),
    ('AB+', 'AB+'),
    ('A-', 'A-'),
    ('B-', 'B-'),
    ('O-', 'O-'),
    ('AB-', 'AB-'),
]


# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, username, reg_num, password=None):
        if not reg_num:
            raise ValueError('Users must have an Registration number ')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            reg_num=reg_num,
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, reg_num, password):
        user = self.create_user(
            reg_num=reg_num,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def upload_location(instance, filename):
    file_path = 'account/{author_id}/profile_pic_{filename}'.format(
        author_id=str(instance.username), filename=filename)
    return file_path


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, )
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    reg_num = models.IntegerField(verbose_name='Registration number', unique=True)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True)
    phone_number = models.IntegerField(null=True, blank=True)
    address = models.TextField(max_length=100, null=True, blank=True)
    blood_group = models.CharField(max_length=3, choices=blood_group_options, null=True, blank=True)

    # USERNAME_FIELD will be what we want to login as email or username
    USERNAME_FIELD = 'username'

    # The fields which must be filled up
    REQUIRED_FIELDS = ['reg_num']

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True
