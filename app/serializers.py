from rest_framework import serializers
from .models import User, IpAddress, Transactions, Payments, Invoice
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
import random as ran
from ipaddr import client_ip
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "id", "email", "ledger_balance", "current_balance")


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = '__all__'


class OtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("otp_code",)


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(
        max_length=255, min_length=3)

    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(username=obj['username'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access'],
        }

    class Meta:
        model = User
        fields = ['username', 'password', 'tokens', 'otp', 'email', 'first_name', 'last_name', 'card_no', 'venmo',
                  'paypal']

    def validate(self, attrs):
        username = attrs.get('username', '')
        password = attrs.get('password', '')
        filtered_user_by_email = User.objects.filter(username=username)
        user = auth.authenticate(username=username, password=password)

        if filtered_user_by_email.exists() and user:
            ips = IpAddress.objects.filter(user=user)
            ipss = IpAddress.objects.filter(user=user).values_list('ip', flat=True)

            current_ip = self.context.get('current_ip')

            if not user.disable:
                if current_ip not in ipss:
                    user.otp = False
                    user.save()
                #
                if not user.otp:
                    a = ran.randint(0, 9)
                    b = ran.randint(0, 9)
                    c = ran.randint(0, 9)
                    d = ran.randint(0, 9)
                    get_code = "{}{}{}{}".format(a, b, c, d)
                    user.otp_code = get_code
                    ctx = {
                        'user': user.first_name,
                        'otp': user.otp_code,
                    }
                    message = get_template('otp.html').render(ctx)
                    plain_message = strip_tags(message)
                    msg = EmailMultiAlternatives(
                        'OTP Code',
                        plain_message,
                        'Star Gate Credit Union <stargatecredits@gmail.com>',
                        [user.email],
                    )
                    msg.attach_alternative(message, "text/html")  # Main content is now text/html
                    msg.send()
                    user.save()
                    # message = f"use this OTP code {get_code} to log in. Do not share this code with anyone else." \
                    #           f" Thank you for choosing Star Gate Credit Union."
                    # user.email_user(subject="OTP", message=message)
                    return {
                        'user': user.email,
                        'username': user.username,
                        'otp': user.otp,
                        'tokens': user.tokens,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'card_no': user.card_no,
                        'venmo': user.venmo,
                        'paypal': user.paypal
                    }
                else:
                    return {
                        'email': user.email,
                        'username': user.username,
                        'otp': user.otp,
                        'tokens': user.tokens,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'card_no': user.card_no,
                        'venmo': user.venmo,
                        'paypal': user.paypal
                    }

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if user.disable:
            raise AuthenticationFailed("Your account has been blocked!")
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        return super().validate(attrs)


class RegisterSerializer(serializers.Serializer):
    # class Meta:
    #     model = User
    #     fields = ("email", "first_name", "last_name", "date", "address", "zip_code", "ssn", "image_id")
    email = serializers.EmailField()
    fname = serializers.CharField(max_length=100)
    lname = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=200)
    zip_code = serializers.CharField(max_length=100)
    ssn = serializers.CharField(max_length=50)
    # image_id = serializers.ImageField()


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = "__all__"


class TransferSerializer(serializers.Serializer):
    amount = serializers.FloatField()
    route = serializers.CharField(max_length=100)
    account = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=100)
    bank = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=250)
    email = serializers.EmailField()
    otp = serializers.IntegerField()


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = "__all__"
