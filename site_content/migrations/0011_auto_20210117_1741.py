# Generated by Django 3.1.5 on 2021-01-17 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("site_content", "0010_auto_20210117_1658"),
    ]

    operations = [
        migrations.AlterField(
            model_name="news",
            name="date",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
