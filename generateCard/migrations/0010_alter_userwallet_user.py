# Generated by Django 4.1.4 on 2023-02-07 10:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("generateCard", "0009_rename_wallet_user_userwallet_user_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userwallet",
            name="user",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
