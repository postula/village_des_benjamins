# Generated by Django 3.1.3 on 2020-11-19 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0004_auto_20201119_1550"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="photo",
            field=models.ImageField(blank=True, null=True, upload_to="members/"),
        ),
    ]
