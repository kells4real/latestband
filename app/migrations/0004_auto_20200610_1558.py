# Generated by Django 2.0.1 on 2020-06-10 14:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_transactions_confirmed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 10, 15, 58, 3, 278496)),
        ),
    ]
