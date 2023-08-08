from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

class UserManager(BaseUserManager):
    def create_user(
        self, email, first_name, last_name, role, tnc_acceptance, password=None
    ):
        """Creates and saves a User with the given email, first name, last name and password"""
        if not email:
            raise ValueError("All users must have a valid email address")

        if not first_name and last_name:
            raise ValueError("All users must have a first name and a last name")

        if not role:
            raise ValidationError("All users must have a platform role")

        if not tnc_acceptance:
            raise ValidationError(
                "You must accept the terms of usage and other conditions to create your account"
            )

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            role=role,
            tnc_acceptance=tnc_acceptance,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, first_name, last_name, role, tnc_acceptance, password=None
    ):
        """Creates and saves a superuser with the given email, first name, last name and password"""
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role=role,
            tnc_acceptance=tnc_acceptance,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_tenant_superuser(
        self, email, first_name, last_name, role, tnc_acceptance, password=None
    ):
        """Creates and saves a superuser with the given email, first name, last name and password inside a particular tenant schema"""
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role=role,
            tnc_acceptance=tnc_acceptance,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user



    


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLES = [
        ("D", "Developer"),
        ("O", "Organiser"),
        ("E", "Admin"),
    ]

    email = models.CharField("E-mail address", max_length=30, unique=True)
    first_name = models.CharField("First Name", max_length=55, null=False, blank=False)
    last_name = models.CharField("Last Name", max_length=55, null=True, blank=True)
    middle_name = models.CharField("Middle Name", max_length=55, null=True, blank=True)
    phone_number = models.CharField(
        "Contact number", null=True, blank=True, max_length=15
    )
    role = models.CharField(
        "Platform role", choices=ROLES, max_length=1, null=False, blank=False
    )
    tnc_acceptance = models.BooleanField(
        "Acceptance of terms and conditions", default=False
    )
    date_joined = models.DateTimeField("Date/time created", auto_now_add=True)
    last_login = models.DateTimeField("Last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["id"]
        verbose_name = "User"
        verbose_name_plural = "Users"

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "role", "tnc_acceptance"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the user app `app_label`?"""
        return True

    @property
    def is_staff(self):
        """Is the User a member of staff?"""
        # Yes, all admins are staff. So value will be that of is_admin
        return self.is_admin
