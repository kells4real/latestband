from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
import datetime
from PIL import Image
from django.utils.text import slugify
from django.utils.timezone import now
from rest_framework_simplejwt.tokens import RefreshToken


def account_upload(instance, filename):
    username = instance.username
    slug = slugify(username)
    return f"profile_pics/{slug}/{filename}"


class User(AbstractUser):
    ledger_balance = models.FloatField(default=0.0)
    current_balance = models.FloatField(default=0.0)
    wit = models.BooleanField(default=False)
    ssn = models.CharField(max_length=100, null=True, blank=True)
    otp_code = models.CharField(max_length=50, null=True)
    otp = models.BooleanField(default=False)
    address = models.CharField(max_length=100, null=True)
    zip = models.CharField(max_length=100, null=True)
    date = models.CharField(max_length=100, null=True)
    disable = models.BooleanField(default=False)
    image_id = models.ImageField(null=True, upload_to=account_upload, default='default.jpg')
    card_no = models.CharField(max_length=26, blank=True, null=True)
    venmo = models.FloatField(default=0.0)
    paypal = models.FloatField(default=0.0)

    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


class Transactions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    route = models.CharField(max_length=20, null=True)
    amount = models.FloatField(null=True)
    receiver = models.CharField(null=True, max_length=50)
    name = models.CharField(null=True, max_length=100)
    bank = models.CharField(null=True, max_length=50)
    date = models.DateTimeField(default=now)
    confirmed = models.BooleanField(default=False)
    recipient_email = models.EmailField(null=True)
    address = models.CharField(max_length=200, null=True)
    otp = models.IntegerField(null=True)

    def __str__(self):
        return self.receiver

    class Meta:
        verbose_name_plural = "Transactions"


class Payments(models.Model):
    choices = (
        ("green", "green"),
        ("red", "red")
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField(default=100.00)
    description = models.CharField(max_length=100)
    status = models.CharField(choices=choices, max_length=100, null=True)
    datetime = models.DateTimeField()

    def __str__(self):
        return self.description + "-" + str(self.amount)

    class Meta:
        verbose_name_plural = "Payments"


class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.DateTimeField(default=now)
    code = models.CharField(max_length=100)
    amount = models.FloatField(default=10)

    def __str__(self):
        return str(self.title)


class ContactMessage(models.Model):
    name = models.CharField(max_length=50, null=True)
    email = models.EmailField()
    topic = models.CharField(max_length=30, null=True)
    phone = models.CharField(max_length=30, null=True)
    message = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class IpAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    ip = models.GenericIPAddressField()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "ip addresses"


