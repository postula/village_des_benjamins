# Generated by Django 3.1.3 on 2020-11-20 10:25

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("holiday", "0009_registration_dates"),
    ]

    operations = [
        migrations.AlterField(
            model_name="registration",
            name="dates",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.DateField(),
                default=list,
                size=None,
                verbose_name="dates",
            ),
        ),
    ]
