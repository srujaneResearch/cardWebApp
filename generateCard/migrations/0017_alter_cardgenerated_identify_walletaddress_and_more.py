# Generated by Django 4.1.4 on 2023-03-11 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("generateCard", "0016_twofaauth_block_twofaauth_block_time_over"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cardgenerated",
            name="identify_walletaddress",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="initialpayment",
            name="identify_walletaddress",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="topupcard",
            name="identify_walletaddress",
            field=models.CharField(max_length=255, null=True),
        ),
    ]
