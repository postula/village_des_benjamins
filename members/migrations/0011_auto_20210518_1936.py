# Generated by Django 3.1.5 on 2021-05-18 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0010_child_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="child",
            name="status",
            field=models.CharField(
                choices=[
                    ("in_validation", "in_validation"),
                    ("registered", "registered"),
                ],
                default="in_validation",
                max_length=50,
                verbose_name="status",
            ),
        ),
    ]
