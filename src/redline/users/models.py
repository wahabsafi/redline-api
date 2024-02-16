from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager as BUM
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from redline.common.models import BaseModel


class BaseUserManager(BUM):
    def create_user(
        self,
        email,
        first_name="",
        last_name="",
        phone_number=None,
        is_active=True,
        is_admin=False,
        password=None,
    ):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email.lower()),
            is_active=is_active,
            is_admin=is_admin,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
        )

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=email,
            is_active=True,
            is_admin=True,
            password=password,
        )

        user.is_superuser = True
        user.save(using=self._db)

        return user


class BaseUser(BaseModel, AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_("First Name"), max_length=50, blank=True)
    last_name = models.CharField(_("Last Name"), max_length=50, blank=True)
    email = models.EmailField(verbose_name=_("Email Address"), unique=True)
    username = models.CharField(_("Username"), max_length=255, unique=True, blank=True)
    phone_number = models.CharField(
        _("Phone Number"), max_length=12, blank=True, null=True
    )
    otp = models.CharField(max_length=6, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_author = models.BooleanField(default=False)

    objects = BaseUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def is_staff(self):
        return self.is_admin

    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        if full_name == " ":
            return self.email
        else:
            return full_name.strip()


class Profile(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    posts_count = models.PositiveIntegerField(default=0)
    subscriber_count = models.PositiveIntegerField(default=0)
    subscription_count = models.PositiveIntegerField(default=0)
    bio = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f"{self.user} >> {self.bio}"
