# Generated by Django 3.1.3 on 2020-11-20 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0006_auto_20201119_1606"),
        ("holiday", "0011_auto_20201120_1510"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="registration",
            unique_together={("holiday", "child")},
        ),
    ]
