# Generated by Django 4.1 on 2022-11-16 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Numerator",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "app_label",
                    models.CharField(max_length=50, verbose_name="application"),
                ),
                ("model", models.CharField(max_length=50, verbose_name="model")),
                (
                    "prefix",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="prefix"
                    ),
                ),
                (
                    "reset_mode",
                    models.CharField(
                        choices=[
                            ("YEAR", "YEARLY"),
                            ("MONTH", "MONTHLY"),
                            ("NEVER", "FIXED"),
                        ],
                        default="YEAR",
                        max_length=50,
                        verbose_name="reset mode",
                    ),
                ),
                ("year", models.IntegerField()),
                ("month", models.IntegerField(default=0)),
                (
                    "counter",
                    models.PositiveIntegerField(default=0, verbose_name="Counter"),
                ),
            ],
            options={
                "verbose_name": "Numerator",
                "verbose_name_plural": "Numerators",
                "unique_together": {
                    ("app_label", "model", "prefix", "reset_mode", "year", "month")
                },
            },
        ),
    ]
