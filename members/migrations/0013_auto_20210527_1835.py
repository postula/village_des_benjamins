# Generated by Django 3.1.5 on 2021-05-27 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0012_user_accept_newsletter"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="accept_newsletter",
            field=models.BooleanField(default=False, verbose_name="accept_newsletter"),
        ),
    ]
