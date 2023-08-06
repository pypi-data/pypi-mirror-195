# Generated by Django 4.1 on 2022-11-16 18:12

import django.db.models.deletion
import mptt.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Menu",
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
                ("url", models.CharField(blank=True, max_length=255, null=True)),
                ("label", models.CharField(max_length=255, verbose_name="label")),
                ("order", models.IntegerField(default=0)),
                ("slug", models.SlugField(max_length=80, unique=True)),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Description"),
                ),
                (
                    "classnames",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="class names",
                    ),
                ),
                ("lft", models.PositiveIntegerField(editable=False)),
                ("rght", models.PositiveIntegerField(editable=False)),
                ("tree_id", models.PositiveIntegerField(db_index=True, editable=False)),
                ("level", models.PositiveIntegerField(editable=False)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this menu belongs to. A menu will get all permissions granted to each of their groups.",
                        related_name="+",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "parent",
                    mptt.fields.TreeForeignKey(
                        blank=True,
                        help_text="Menu Item can have a hierarchy. You might have a Music Item, and under that have children items for Jazz and Blues. Totally optional.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="children",
                        to="coreplus_navigators.menu",
                    ),
                ),
            ],
            options={
                "verbose_name": "Menu",
                "verbose_name_plural": "Menus",
            },
        ),
        migrations.CreateModel(
            name="Placeholder",
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
                ("name", models.CharField(max_length=255, verbose_name="name")),
                ("slug", models.SlugField(max_length=80, unique=True)),
                (
                    "template_name",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="template"
                    ),
                ),
                ("template_string", models.TextField(blank=True, null=True)),
                (
                    "menu_root",
                    mptt.fields.TreeForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to="coreplus_navigators.menu",
                    ),
                ),
            ],
            options={
                "verbose_name": "Placeholder",
                "verbose_name_plural": "Placeholders",
            },
        ),
    ]
