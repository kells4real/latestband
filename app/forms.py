from django import forms
from .models import Transactions, User
import re
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class TransactionForm(forms.ModelForm):

    amount = forms.RegexField(regex=re.compile(r'^[1-9][0-9]*$'), required=True,
                              error_messages={'invalid': "Enter a valid amount, must be 50 and above"},
                              label="Amount in USD")

    receiver = forms.RegexField(regex=re.compile(r'^[0-9]{8,12}$'), required=True,
                              error_messages={'invalid': "Enter a valid amount, must be 50 and above"},
                              label="Account No")
    class Meta:
        model = Transactions
        fields = ["receiver", "name", "bank", "amount", "route"]

        labels = {
            "receiver": "Receiver's Account No",
            "name": "Receiver's Name",
            "bank": "Receiver's Bank Name",
            "route": "Routing Number"
        }


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('ledger_balance', 'current_balance', 'wit')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('ledger_balance', 'current_balance', 'wit')

