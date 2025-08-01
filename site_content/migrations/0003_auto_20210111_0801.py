# Generated by Django 3.1.5 on 2021-01-11 08:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("site_content", "0002_auto_20210111_0720"),
    ]

    operations = [
        migrations.CreateModel(
            name="Content",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="name")),
                (
                    "icon",
                    models.CharField(
                        blank=True,
                        help_text="https://fontawesome.com/v4.7.0/icons/",
                        max_length=255,
                        null=True,
                        verbose_name="icon",
                    ),
                ),
                ("description", models.TextField(verbose_name="description")),
            ],
            options={
                "verbose_name": "content",
                "verbose_name_plural": "content",
            },
        ),
        migrations.CreateModel(
            name="SiteSection",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="name")),
            ],
            options={
                "verbose_name": "site_section",
                "verbose_name_plural": "site_sections",
            },
        ),
        migrations.DeleteModel(
            name="Service",
        ),
        migrations.AddField(
            model_name="content",
            name="section",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="site_content.sitesection",
                verbose_name="site_section",
            ),
        ),
    ]
