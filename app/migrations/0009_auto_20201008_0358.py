# Generated by Django 2.1.5 on 2020-10-08 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_transactions_route'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='otp',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='otp_code',
            field=models.IntegerField(null=True),
        ),
    ]
