# Generated by Django 4.1.4 on 2023-02-02 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("generateCard", "0007_initialpayment_card_holder_addressline1_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="cardgenerated",
            name="card_holder_state",
            field=models.CharField(default=840, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="initialpayment",
            name="card_holder_state",
            field=models.CharField(default=840, max_length=30),
            preserve_default=False,
        ),
    ]
