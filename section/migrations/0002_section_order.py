# Generated by Django 3.1.5 on 2021-05-19 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("section", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="section",
            name="order",
            field=models.PositiveIntegerField(
                db_index=True, default=1, editable=False, verbose_name="order"
            ),
            preserve_default=False,
        ),
    ]
