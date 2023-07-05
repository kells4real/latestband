from django.urls import path
from .views import client, transaction_list, transfer, transaction, otp, transfer_successful,\
    accountDetails, LoginAPIView, transactionsList, paymentsList, recentTransactionsList,\
    getOtp, invoice, morePaymentsList, authenticateCheck
import random as ran


urlpatterns = [
    path('', client, name='client'),
    # path('transactions/', transaction_list, name='transactions'),
    path('transfer/', transfer, name="transfer"),
    path('transfer_successful/', transfer_successful, name='transfer-successful'),
    path('account_details/', accountDetails, name='account-details'),
    path('transactions/', transactionsList, name='transactions-list'),
    path('transaction/', recentTransactionsList, name='recent-transactions-list'),
    path('payments/', paymentsList, name='payments-list'),
    path('payments_all/', morePaymentsList, name='payments-list'),
    path('otp/', otp, name="otp"),
    path('login/', LoginAPIView.as_view(), name="api-login"),
    path('get-otp/', getOtp, name="get-otp"),
    path('invoices/', invoice, name="invoices"),
    path('authenticate/', authenticateCheck, name="authenticate"),
    # path(f"transaction/<int:pk>/{ran.randint(1, 900000)}/", transaction, name="transaction")
]
