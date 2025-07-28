from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(
            self,
            email,
            first_name,
            last_name,
            phone_number,
            gender,
            password=None,
    ) -> "User":
        if not email:
            raise ValueError("An email is required.")
        if not password:
            raise ValueError("A password is required.")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            gender=gender,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
            self,
            email,
            password,
            first_name,
            last_name,
            phone_number,
            gender,
    ) -> "User":
        if not email:
            raise ValueError("An email is required.")
        if not password:
            raise ValueError("A password is required.")
        user = self.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            gender=gender,
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True

        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    gender = models.CharField(
        max_length=1,
        choices={"m": "male", "f": "female", "u": "unknown"},
        null=True,
        blank=True,
    )
    phone_number = models.CharField(max_length=15, unique=True)
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "phone_number",
        "gender",
    ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class City(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Cities"


class Tours(models.Model):
    departure_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="departure_city")
    arrive_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="arrive_city")
    departure_to_time = models.DateTimeField()  # Відправлення до міста відпочинку
    departure_from_time = models.DateTimeField()  # Відправлення з міста відпочинку
    price = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to="tours_photos")

    def __str__(self):
        return f"{self.departure_city} - {self.arrive_city}"

    class Meta:
        verbose_name_plural = "Tours"


class Rate(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tours, on_delete=models.CASCADE, default=None)
    stars = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ]
    )
    comment = models.CharField(max_length=512, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author}, {self.created_at}"


class News(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    image = models.ImageField(upload_to="news_photos")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name_plural = "News"


class Books(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    tour = models.ForeignKey(Tours, on_delete=models.CASCADE, default=None)
    booked_at = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.user} {self.tour} {self.booked_at}"

    class Meta:
        verbose_name_plural = "Books"
