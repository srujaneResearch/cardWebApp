# Generated by Django 4.1.4 on 2023-01-23 10:44

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CardGenerated",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("card_holder_user", models.IntegerField()),
                ("card_holder_surname", models.CharField(max_length=40)),
                ("card_holder_name", models.CharField(max_length=40)),
                ("card_holder_addressline1", models.TextField()),
                ("card_holder_city", models.CharField(max_length=30)),
                ("card_holder_country", models.CharField(max_length=50)),
                ("card_holder_zip", models.IntegerField()),
                ("card_number", models.BigIntegerField()),
                ("card_expiry_month", models.IntegerField()),
                ("card_cvv", models.IntegerField()),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="CardTypes",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("card_type", models.IntegerField()),
                ("card_name", models.CharField(max_length=200)),
                ("card_currency", models.CharField(max_length=6)),
                ("card_generatefee", models.IntegerField()),
                ("card_topup_fixfee", models.IntegerField()),
                ("card_topup_percentfee", models.IntegerField()),
                ("card_monthly_fee", models.FloatField()),
                ("card_balance_limit", models.BigIntegerField()),
                ("card_transaction_limit", models.BigIntegerField()),
                ("card_kyc", models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name="InitialPayment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user_name", models.IntegerField()),
                (
                    "amount",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(50),
                            django.core.validators.MaxValueValidator(5000),
                        ]
                    ),
                ),
                ("payment_amount", models.FloatField()),
                ("coinpayment_fees", models.FloatField(default=0.75)),
                (
                    "payment_type",
                    models.CharField(
                        choices=[("manual", "manual"), ("coinpayment", "coinpayment")],
                        max_length=12,
                    ),
                ),
                ("coinpayment_tx_hash", models.CharField(max_length=255)),
                (
                    "payment_status",
                    models.CharField(
                        choices=[
                            ("initiated", "initiated"),
                            ("rejected", "rejected"),
                            ("successful", "successful"),
                            ("approved", "approved"),
                            ("pending", "pending"),
                        ],
                        max_length=15,
                    ),
                ),
                ("payed_from_wallet_address", models.CharField(max_length=255)),
                ("payed_transaction_hash", models.CharField(max_length=255)),
                ("timestamp_initiated", models.DateTimeField(auto_now_add=True)),
                ("timestamp_finished", models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name="TopupCard",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("from_user", models.IntegerField()),
                ("amount", models.FloatField()),
                ("payment_amount", models.FloatField()),
                ("coinpayment_fees", models.FloatField(default=0.75)),
                (
                    "payment_type",
                    models.CharField(
                        choices=[("manual", "manual"), ("coinpayment", "coinpayment")],
                        max_length=12,
                    ),
                ),
                ("coinpayment_tx_hash", models.CharField(max_length=255)),
                (
                    "payment_status",
                    models.CharField(
                        choices=[
                            ("initiated", "initiated"),
                            ("rejected", "rejected"),
                            ("successful", "successful"),
                            ("approved", "approved"),
                            ("pending", "pending"),
                        ],
                        max_length=15,
                    ),
                ),
                ("payed_from_wallet_address", models.CharField(max_length=255)),
                ("payed_transaction_hash", models.CharField(max_length=255)),
                ("timestamp_initiated", models.DateTimeField(auto_now_add=True)),
                ("timestamp_finished", models.DateTimeField()),
                (
                    "card",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="generateCard.cardgenerated",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="cardgenerated",
            name="card_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="generateCard.cardtypes"
            ),
        ),
        migrations.AddField(
            model_name="cardgenerated",
            name="initial_payment_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="generateCard.initialpayment",
            ),
        ),
    ]
