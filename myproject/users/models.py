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


ROLES = [
    ("D", "Developer"),
    ("O", "Organiser"),
    ("E", "Admin"),
]


class CustomUser(AbstractBaseUser, PermissionsMixin):
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

    def has_module_perm(self, app_label):
        """Does the user have permissions to view the user app `app_label`?"""
        return True

    @property
    def is_staff(self):
        """Is the User a member of staff?"""
        # Yes, all admins are staff. So value will be that of is_admin
        return self.is_admin


# Profile model (only for Realestate entities)
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     profile_picture = models.FileField(
#         "Your profile picture", null=True, blank=True, upload_to="", max_length=255
#     )
#     address_line_1 = models.CharField(
#         "Door/plot no.", max_length=55, null=True, blank=True
#     )
#     address_line_2 = models.CharField(
#         "Building/sub-building", max_length=55, null=True, blank=True
#     )
#     address_line_3 = models.CharField(
#         "Street address", max_length=55, null=True, blank=True
#     )
#     address_line_4 = models.CharField(
#         "Area/Locality/Town", max_length=55, null=True, blank=True
#     )
#     # import city data package
#     # city = models.ForeignKey(City, default=None, null=True, blank=True, on_delete=models.DO_NOTHING)
#     # state = models.ForeignKey(Region, on_delete=models.DO_NOTHING, verbose_name="Province/Region/State")
#     # country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)
#     zip_code = models.CharField(
#         "PIN/ZIP code", default=None, max_length=20, null=True, blank=True
#     )
#     pan_id = models.CharField(
#         "Taxpayer Identification Number(TIN)", max_length=15, null=True, blank=True
#     )
#     pan_id_proof = models.FileField(
#         "Upload an image of the TIN", null=True, blank=True, upload_to=""
#     )
#     # A forgotten field for government identifier by a number or a sequence was missing. Hence, it has been added on 04th of April, 2023.
#     govt_id = models.CharField(
#         "Government Identification Number",
#         max_length=50,
#         default=None,
#         blank=True,
#         null=True,
#     )
#     # add id choices
#     govt_id_type = models.CharField(
#         "Type of Govt. authorized ID",
#         choices=ID_CHOICES,
#         max_length=1,
#         null=True,
#         blank=True,
#     )  # Required only for landlord
#     govt_id_proof = models.FileField(
#         "Upload an image of the type of ID specified",
#         max_length=255,
#         upload_to="",
#         null=True,
#         blank=True,
#         max_file_size=4194304,
#     )  # Required only for landlord. Max file size limited to 4MB

#     def __str__(self):
#         return f"User profile for {self.user.first_name} {self.user.last_name}"

#     class Meta:
#         verbose_name = "Profile"
#         verbose_name_plural = "Profiles"
#         ordering = ["id"]
