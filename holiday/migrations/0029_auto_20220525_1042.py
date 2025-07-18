# Generated by Django 3.1.5 on 2022-05-25 10:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("holiday", "0028_holiday_book_by_day"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="outing",
            options={
                "ordering": ["start_date"],
                "verbose_name": "outing",
                "verbose_name_plural": "outings",
            },
        ),
        migrations.RenameField(
            model_name="outing",
            old_name="date",
            new_name="start_date",
        ),
    ]
