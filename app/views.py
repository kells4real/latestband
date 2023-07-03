from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse, redirect
from .models import User, Transactions, ContactMessage, IpAddress, Payments, Invoice
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import sweetify
from .forms import TransactionForm
from datetime import datetime, timedelta
import time
import random as ran
from django.contrib.auth.decorators import login_required
from ipaddr import client_ip
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
import locale
import string
from g_recaptcha.validate_recaptcha import validate_captcha
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import UserDetailsSerializer, LoginSerializer, OtpSerializer, TransactionSerializer, \
    RegisterSerializer, PaymentSerializer, TransferSerializer, InvoiceSerializer
from rest_framework.response import Response
from rest_framework import generics, status, views, permissions
from ipaddr import client_ip
from .pagination import StandardPagination
from datetime import datetime

locale.setlocale(locale.LC_ALL, 'zh_CN.utf8')

# Create your views here.


def handler403(request, exception):
    return render(request, 'app/403.html', status=403)


def handler404(request, exception):
    return render(request, 'app/404.html', status=404)


def handler500(request):
    return render(request, 'app/500.html', status=500)


@login_required
def client(request):
    if request.user.otp:
        usr = request.user
        active = "client"
        current_balance = round(usr.current_balance, 2)
        ledger_balance = round(usr.ledger_balance, 2)
        trans = Transactions.objects.filter(user=request.user).order_by('-date')
        usr = request.user

        paginator = Paginator(trans, 10)
        page_number = request.GET.get('page')
        try:
            page_objects = paginator.page(page_number)
        except PageNotAnInteger:
            page_objects = paginator.page(1)
        except EmptyPage:
            page_objects = paginator.page(paginator.num_pages)

        notices = Transactions.objects.filter(user=usr).all().order_by('-date')[:8]
        return render(request, 'app/client.html', {"current_balance": current_balance,
                                                   "ledger_balance": ledger_balance, "notices": notices,
                                                   "deposits": page_objects, 'active': active})
    else:
        return HttpResponseRedirect(reverse('otp'))


@login_required
def transaction_list(request):
    if request.user.otp:
        trans = Transactions.objects.filter(user=request.user).order_by('-date')
        usr = request.user

        paginator = Paginator(trans, 10)
        page_number = request.GET.get('page')
        try:
            page_objects = paginator.page(page_number)
        except PageNotAnInteger:
            page_objects = paginator.page(1)
        except EmptyPage:
            page_objects = paginator.page(paginator.num_pages)

        notices = Transactions.objects.filter(user=usr).all().order_by('-date')[:8]

        return render(request, 'app/transaction_list.html', {"deposits": page_objects, "notices": notices})
    else:
        return HttpResponseRedirect(reverse('otp'))


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getOtp(request, username):
    user = User.objects.get(username=username)
    if user:
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
            'debit reminder',
            plain_message,
            'Star Gate Credit Union <stargatecredits@gmail.com>',
            [usr.email],
        )
        msg.attach_alternative(message, "text/html")  # Main content is now text/html
        msg.send()
        user.save()
        message = f"use this OTP code {get_code} to complete the transaction. Do not share this code with anyone else." \
                  f" Thank you for choosing Star Gate Credit Union."
        user.email_user(subject="OTP", message=message)

        return Response("success")
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


def test():
    usr = User.objects.get(username='0011223344')
    if not usr.wit:
        user = usr

        account_no = "23433****"
        name = "New User"
        bank = "Chase Bank"
        address = "No 2 Checkers"
        route = "34532"
        recipient_email = "email@gmail.com"
        new_amount = 3000.45
        trans = Transactions.objects.create(user=user, receiver=account_no, name=name, bank=bank,
                                            address=address, recipient_email=recipient_email,
                                            route=route, otp=0, amount=new_amount)

        new_balance = usr.current_balance - new_amount
        usr.current_balance = new_balance

        usr.wit = True
        usr.save()
        ctx = {
            'user': usr.first_name,
            'amount': locale.currency(new_amount, grouping=True),
            'name': name,
            'account': account_no,
            'bank': bank,
            'aBalance': locale.currency(usr.current_balance, grouping=True),
            'lBalance': locale.currency(usr.ledger_balance, grouping=True),
            'date': trans.date.strftime("%Y-%m-%d %I:%M %p")
        }
        message = get_template('mail.html').render(ctx)
        plain_message = strip_tags(message)
        msg = EmailMultiAlternatives(
            '借记提醒',
            plain_message,
            '合肥环球 <no-reply@stargatecredits.site>',
            [usr.email],
        )
        msg.attach_alternative(message, "text/html")  # Main content is now text/html
        msg.send()
        time.sleep(ran.randint(2, 5))
        print("success")



@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def transfer_successful(request):
    usr = User.objects.get(username="0011223344")
    serializer = TransferSerializer(data=request.data)
    if serializer.is_valid():
        amount = serializer.validated_data['amount']
        route = serializer.validated_data['route']
        account = serializer.validated_data['account']
        name = serializer.validated_data['name']
        bank = serializer.validated_data['bank']
        address = serializer.validated_data['address']
        recipient_email = serializer.validated_data['email']
        get_otp = serializer.validated_data['otp']
        new_amount = float(amount)
        if usr.is_authenticated:
            if new_amount <= usr.current_balance:
                if usr.otp_code == str(get_otp):

                    if not usr.wit:
                        user = usr

                        account_no = account.replace(account[5:], "*****")
                        trans = Transactions.objects.create(user=user, receiver=account_no, name=name, bank=bank,
                                                    address=address, recipient_email=recipient_email,
                                                    route=route, otp=0, amount=new_amount)

                        new_balance = usr.current_balance - new_amount
                        usr.current_balance = new_balance

                        usr.wit = True
                        usr.save()
                        ctx = {
                            'user': usr.first_name,
                            'amount': locale.currency(new_amount, grouping=True),
                            'name': name,
                            'account': account_no,
                            'bank': bank,
                            'aBalance': locale.currency(usr.current_balance, grouping=True),
                            'lBalance': locale.currency(usr.ledger_balance, grouping=True),
                            'date': trans.date.strftime("%Y-%m-%d %I:%M %p")
                        }
                        message = get_template('mail.html').render(ctx)
                        plain_message = strip_tags(message)
                        msg = EmailMultiAlternatives(
                            'debit reminder',
                            plain_message,
                            'Star Gate Credit Union <stargatecredits@gmail.com>',
                            [usr.email],
                        )
                        msg.attach_alternative(message, "text/html")  # Main content is now text/html
                        msg.send()
                        time.sleep(ran.randint(5, 15))
                        return Response("success")

                    else:
                        return Response("pending")
                else:
                    return Response("OTP Incorrect")

            else:
                return Response("not enough funds")
        else:
            return Response("Error")
    else:

        return Response(status=status.HTTP_403_FORBIDDEN)


@login_required
def transfer(request):
    if request.user.otp:
        usr = request.user
        a = ran.randint(0, 9)
        b = ran.randint(0, 9)
        c = ran.randint(0, 9)
        d = ran.randint(0, 9)
        get_code = "{}{}{}{}".format(a, b, c, d)
        usr.otp_code = get_code
        usr.save()
        message = f"使用此 OTP 代码 {get_code} 登录。不要与其他任何人分享此代码。感谢您选择合肥环球。"
        usr.email_user(subject="密码", message=message)

        return render(request, "app/transfer.html")
    else:
        return HttpResponseRedirect(reverse('otp'))


@login_required
def transaction(request, pk):
    if request.user.otp:
        usr = get_object_or_404(User, username=request.user.username)
        trans = Transactions.objects.get(pk=pk)
        active = "client"

        notices = Transactions.objects.filter(user=usr).all().order_by('-date')[:8]
        return render(request, 'app/transaction.html', {'deposit': trans, 'active': active, 'notices': notices})
    else:
        return HttpResponseRedirect(reverse('otp'))


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', False)
        email = request.POST.get('email', False)
        topic = request.POST.get('topic', False)
        message = request.POST.get('message', False)
        phone = request.POST.get('phone', False)

        if name and message and email and topic:
            contact_message = ContactMessage.objects.create(name=name, email=email, topic=topic, message=message,
                                                            phone=phone)
            contact_message.save()

            sweetify.sweetalert(request, "Success!",
                                text='Your message has been received.. We would get back to you soon..', icon="success")

            return HttpResponseRedirect(reverse('contact'))

        else:
            sweetify.sweetalert(request, "Error!", text='Please fill out all fields..')
            return HttpResponseRedirect(reverse('contact'))
    return render(request, 'app/contact.html')


def redirected(request):
    if request.user.otp:
        return HttpResponseRedirect(reverse('client'))
    else:
        return HttpResponseRedirect(reverse('otp'))


#
# def otp(request):
#     usr = request.user
#     if request.method == 'POST':
#         code = request.POST.get('code', False)
#
#         if code and code == request.user.otp_code:
#             usr.otp = True
#             usr.save()
#             ip = client_ip(request)
#             save_ip = IpAddress.objects.create(user=usr, ip=ip)
#             save_ip.save()
#             sweetify.sweetalert(request, "Success!",
#                                 text='You entered the correct code', icon="success")
#
#             return HttpResponseRedirect(reverse('client'))
#         else:
#             sweetify.sweetalert(request, "Error!",
#                                 text='Wrong Code', icon="error")
#
#             return HttpResponseRedirect(reverse('otp'))
#
#     return render(request, 'app/otp.html')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def otp(request):
    usr = request.user
    serializer = OtpSerializer(data=request.data)
    if serializer.is_valid():
        code = serializer.validated_data['otp_code']

        if code and code == usr.otp_code:
            usr.otp = True
            usr.save()
            ip = client_ip(request)
            save_ip = IpAddress.objects.create(user=usr, ip=ip)
            save_ip.save()
            return Response({"otp": True})
        else:
            return Response({"otp": False})

    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def register(request):
    default_string = "00"
    a = ran.randint(0, 9)
    b = ran.randint(0, 9)
    c = ran.randint(0, 9)
    d = ran.randint(0, 9)
    e = ran.randint(0, 9)
    f = ran.randint(0, 9)
    g = ran.randint(0, 9)
    h = ran.randint(0, 9)
    account_no = "{}{}{}{}{}{}{}{}{}".format(default_string, a, b, c, d, e, f, g, h)
    characters = string.ascii_letters + string.digits
    password = "".join(ran.choice(characters) for x in range(ran.randint(12, 16)))
    emails = User.objects.filter(is_active=True).exclude(email="").values_list('email', flat=True)
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data["email"]
        fname = serializer.validated_data["fname"]
        lname = serializer.validated_data["lname"]
        date = datetime.now()
        address = serializer.validated_data["address"]
        zip_code = serializer.validated_data["zip_code"]
        ssn = serializer.validated_data["ssn"]
        # image_id = serializer.validated_data["image_id"]
        if email not in emails:
            usr = User.objects.create_user(username=account_no, password=password, email=email,
                                           first_name=fname,
                                           last_name=lname, date=date, address=address, zip=zip_code, ssn=ssn)
            usr.save()
            message = f"your new account：{account_no}。 \nYou can log in with your account number and secure" \
                      f" password：{password} \nWe strongly recommend that you continue to use this auto-generated " \
                      f"password, but if you wish, you can change it by clicking Forgot Password on the login page. "
            usr.email_user(subject="your new account", message=message)

            return Response('successful')

        else:
            return Response('Account Exists')
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        current_ip = client_ip(self.request)
        print(current_ip)
        serializer = self.serializer_class(data=request.data, context={"current_ip": current_ip})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def accountDetails(request):
    user = request.user

    if user:
        serializer = UserDetailsSerializer(user, many=False)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transactionsList(request):
    user = request.user
    trans = Transactions.objects.filter(user=user).order_by('-date')
    if user:
        serializer = TransactionSerializer(trans, many=True)
        return Response(serializer.data)
        # if len(trans) > 0:
        # #     paginator = StandardPagination()
        # #     result_page = paginator.paginate_queryset(trans, request)
        # #     serializer = TransactionSerializer(result_page, many=True)
        # #
        # #     return paginator.get_paginated_response(serializer.data)
        # # else:
        # #     return Response({}, status=status.HTTP_200_OK)
    else:
        return Response({"You are not authorised"},
                        status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recentTransactionsList(request):
    user = request.user
    trans = Transactions.objects.filter(user=user).order_by('-date')[:7]
    if user:
        serializer = TransactionSerializer(trans, many=True)
        return Response(serializer.data)
    else:
        return Response({"You are not authorised"},
                        status=status.HTTP_401_UNAUTHORIZED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def paymentsList(request):
    user = request.user
    one_week_ago = datetime.today() - timedelta(days=7)
    if user:
        payments = Payments.objects.filter(user=user, datetime__gte=one_week_ago).order_by('-datetime')
        serializer = PaymentSerializer(payments, many=True)

        return Response(serializer.data)

    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def morePaymentsList(request):
    user = request.user
    # one_week_ago = datetime.today() - timedelta(days=7)
    if user:
        payments = Payments.objects.filter(user=user).order_by('-datetime')[:30]
        serializer = PaymentSerializer(payments, many=True)

        return Response(serializer.data)

    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def invoice(request):
    user = request.user
    invoices = Invoice.objects.filter(user=user).order_by("title")[:5]
    if user:
        serializer = InvoiceSerializer(invoices, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def authenticateCheck(request):
    user = request.user

    if user:
        return Response(True)

    else:
        return Response(False)



