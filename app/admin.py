from django.contrib import admin
from .models import Transactions, User, IpAddress, Payments, Invoice
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (  # new fieldset added on to the bottom
            'Custom Field Heading',  # group heading of your choice; set to None for a blank space instead of a header
            {
                'fields': (
                    'ledger_balance', 'current_balance', 'wit', 'ssn', 'otp', 'otp_code', 'address', 'zip', 'date',
                    'disable', 'image_id', 'card_no', 'venmo', 'paypal'
                ),
            },
        ),
    )

    def get_queryset(self, request):
        query = super(UserAdmin, self).get_queryset(request)
        query_set = query.filter(is_superuser=False)
        return query_set


admin.site.register(User, CustomUserAdmin)

admin.site.register(Transactions)
admin.site.register(IpAddress)
admin.site.register(Payments)
admin.site.register(Invoice)
