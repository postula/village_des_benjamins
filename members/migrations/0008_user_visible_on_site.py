# Generated by Django 3.1.5 on 2021-01-11 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0007_auto_20210111_0720"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="visible_on_site",
            field=models.BooleanField(default=False, verbose_name="visible_on_site"),
        ),
    ]
