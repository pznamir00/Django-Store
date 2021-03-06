# Generated by Django 3.2.6 on 2021-09-16 16:47

import address.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('address', '0004_auto_20210916_1746'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
                ('score', models.PositiveIntegerField(default=0)),
                ('joined', models.DateTimeField(auto_now_add=True)),
                ('address', address.models.AddressField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='address.address')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
