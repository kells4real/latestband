# Generated by Django 2.1.5 on 2022-05-19 22:06

import app.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_auto_20210110_1843'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.DateTimeField(default=django.utils.timezone.now)),
                ('code', models.CharField(max_length=100)),
                ('amount', models.FloatField(default=10)),
            ],
        ),
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=100.0)),
                ('description', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('green', 'green'), ('red', 'red')], max_length=100, null=True)),
                ('datetime', models.DateTimeField()),
            ],
            options={
                'verbose_name_plural': 'Payments',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='card_no',
            field=models.CharField(blank=True, max_length=26, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='paypal',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='user',
            name='venmo',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='otp',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='image_id',
            field=models.ImageField(default='default.jpg', null=True, upload_to=app.models.account_upload),
        ),
        migrations.AddField(
            model_name='payments',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='invoice',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
