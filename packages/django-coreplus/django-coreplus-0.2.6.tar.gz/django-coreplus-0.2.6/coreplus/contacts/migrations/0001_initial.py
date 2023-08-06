# Generated by Django 4.1 on 2022-11-16 18:18

import django.db.models.deletion
import phonenumber_field.modelfields
from django.db import migrations, models

import coreplus.utils.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Country",
            fields=[
                (
                    "iso_3166_1_a2",
                    models.CharField(
                        max_length=2,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ISO 3166-1 alpha-2",
                    ),
                ),
                (
                    "iso_3166_1_a3",
                    models.CharField(
                        blank=True, max_length=3, verbose_name="ISO 3166-1 alpha-3"
                    ),
                ),
                (
                    "iso_3166_1_numeric",
                    models.CharField(
                        blank=True, max_length=3, verbose_name="ISO 3166-1 numeric"
                    ),
                ),
                (
                    "printable_name",
                    models.CharField(
                        db_index=True, max_length=128, verbose_name="Country name"
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=128, verbose_name="Official name"),
                ),
                (
                    "display_order",
                    models.PositiveSmallIntegerField(
                        db_index=True,
                        default=0,
                        help_text="Higher the number, higher the country in the list.",
                        verbose_name="Display order",
                    ),
                ),
                (
                    "is_shipping_country",
                    models.BooleanField(
                        db_index=True, default=False, verbose_name="Is shipping country"
                    ),
                ),
            ],
            options={
                "verbose_name": "Country",
                "verbose_name_plural": "Countries",
                "ordering": ("-display_order", "printable_name"),
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ShippingAddress",
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
                    "address",
                    models.CharField(max_length=255, null=True, verbose_name="address"),
                ),
                (
                    "city",
                    models.CharField(max_length=255, null=True, verbose_name="city"),
                ),
                (
                    "state",
                    models.CharField(
                        max_length=255, null=True, verbose_name="province"
                    ),
                ),
                (
                    "postcode",
                    coreplus.utils.models.fields.UppercaseCharField(
                        blank=True, max_length=64, verbose_name="Post/Zip-code"
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        choices=[
                            ("Mr", "Mr"),
                            ("Miss", "Miss"),
                            ("Mrs", "Mrs"),
                            ("Ms", "Ms"),
                            ("Dr", "Dr"),
                        ],
                        help_text="Treatment Pronouns for the contact",
                        max_length=64,
                        null=True,
                        verbose_name="Title",
                    ),
                ),
                (
                    "contact",
                    models.CharField(
                        help_text="Contact name will be used.",
                        max_length=255,
                        null=True,
                        verbose_name="contact",
                    ),
                ),
                (
                    "phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True,
                        help_text="In case we need to call you about your order",
                        max_length=128,
                        region=None,
                        verbose_name="Phone number",
                    ),
                ),
                (
                    "loc_name",
                    models.CharField(
                        choices=[
                            ("home", "Home"),
                            ("office", "Office"),
                            ("branch_office", "Branch Office"),
                            ("billing", "Billing"),
                            ("shipping", "Shipping"),
                            ("drop_shipping", "Dropshipping"),
                            ("deliverable", "Deliverable"),
                            ("else", "Else"),
                        ],
                        default="billing",
                        help_text="E.g. Shipping or billing",
                        max_length=255,
                        verbose_name="name",
                    ),
                ),
                (
                    "loc_name_custom",
                    models.CharField(
                        blank=True,
                        help_text="Other location name. E.g. Basecamp",
                        max_length=255,
                        null=True,
                        verbose_name="other name",
                    ),
                ),
                ("primary", models.BooleanField(default=False)),
                (
                    "notes",
                    models.TextField(
                        blank=True,
                        help_text="Tell us anything we should know when delivering your order.",
                        verbose_name="Instructions",
                    ),
                ),
                (
                    "content_id",
                    models.IntegerField(
                        blank=True, help_text="Linked order primary key.", null=True
                    ),
                ),
                (
                    "content_type",
                    models.ForeignKey(
                        blank=True,
                        help_text="Linked order",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="shipping_addresses",
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "country",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="coreplus_contacts.country",
                        verbose_name="Country",
                    ),
                ),
            ],
            options={
                "verbose_name": "Shipping address",
                "verbose_name_plural": "Shipping addresses",
            },
        ),
        migrations.CreateModel(
            name="LinkedContact",
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
                    "contact_type",
                    models.CharField(
                        choices=[
                            ("phone", "Phone"),
                            ("fax", "Fax"),
                            ("mobile", "Mobile"),
                            ("whatsapp", "Whatsapp"),
                            ("telegram", "Telegram"),
                        ],
                        default="phone",
                        help_text="E.g. Phone or mobile",
                        max_length=255,
                        verbose_name="type",
                    ),
                ),
                (
                    "contact",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True,
                        help_text="Contact number",
                        max_length=128,
                        region=None,
                        verbose_name="Phone number",
                    ),
                ),
                ("is_verified", models.BooleanField(default=False, editable=False)),
                (
                    "linked_object_id",
                    models.IntegerField(
                        blank=True, help_text="Linked instance primary key.", null=True
                    ),
                ),
                (
                    "linked_object_type",
                    models.ForeignKey(
                        blank=True,
                        help_text="Linked object type",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="linked_contacts",
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="LinkedAddress",
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
                    "address",
                    models.CharField(max_length=255, null=True, verbose_name="address"),
                ),
                (
                    "city",
                    models.CharField(max_length=255, null=True, verbose_name="city"),
                ),
                (
                    "state",
                    models.CharField(
                        max_length=255, null=True, verbose_name="province"
                    ),
                ),
                (
                    "postcode",
                    coreplus.utils.models.fields.UppercaseCharField(
                        blank=True, max_length=64, verbose_name="Post/Zip-code"
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        choices=[
                            ("Mr", "Mr"),
                            ("Miss", "Miss"),
                            ("Mrs", "Mrs"),
                            ("Ms", "Ms"),
                            ("Dr", "Dr"),
                        ],
                        help_text="Treatment Pronouns for the contact",
                        max_length=64,
                        null=True,
                        verbose_name="Title",
                    ),
                ),
                (
                    "contact",
                    models.CharField(
                        help_text="Contact name will be used.",
                        max_length=255,
                        null=True,
                        verbose_name="contact",
                    ),
                ),
                (
                    "phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True,
                        help_text="In case we need to call you about your order",
                        max_length=128,
                        region=None,
                        verbose_name="Phone number",
                    ),
                ),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True,
                        help_text="In case we need to call you about your order",
                        max_length=128,
                        region=None,
                        verbose_name="Phone number",
                    ),
                ),
                (
                    "notes",
                    models.TextField(
                        blank=True,
                        help_text="Tell us anything we should know.",
                        verbose_name="Note",
                    ),
                ),
                (
                    "linked_object_id",
                    models.IntegerField(
                        blank=True, help_text="Linked instance primary key.", null=True
                    ),
                ),
                (
                    "country",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="coreplus_contacts.country",
                        verbose_name="Country",
                    ),
                ),
                (
                    "linked_object_type",
                    models.ForeignKey(
                        blank=True,
                        help_text="Linked object type",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="linked_addresses",
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="DeliverableAddress",
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
                    "address",
                    models.CharField(max_length=255, null=True, verbose_name="address"),
                ),
                (
                    "city",
                    models.CharField(max_length=255, null=True, verbose_name="city"),
                ),
                (
                    "state",
                    models.CharField(
                        max_length=255, null=True, verbose_name="province"
                    ),
                ),
                (
                    "postcode",
                    coreplus.utils.models.fields.UppercaseCharField(
                        blank=True, max_length=64, verbose_name="Post/Zip-code"
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        choices=[
                            ("Mr", "Mr"),
                            ("Miss", "Miss"),
                            ("Mrs", "Mrs"),
                            ("Ms", "Ms"),
                            ("Dr", "Dr"),
                        ],
                        help_text="Treatment Pronouns for the contact",
                        max_length=64,
                        null=True,
                        verbose_name="Title",
                    ),
                ),
                (
                    "contact",
                    models.CharField(
                        help_text="Contact name will be used.",
                        max_length=255,
                        null=True,
                        verbose_name="contact",
                    ),
                ),
                (
                    "phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True,
                        help_text="In case we need to call you about your order",
                        max_length=128,
                        region=None,
                        verbose_name="Phone number",
                    ),
                ),
                (
                    "loc_name",
                    models.CharField(
                        choices=[
                            ("home", "Home"),
                            ("office", "Office"),
                            ("branch_office", "Branch Office"),
                            ("billing", "Billing"),
                            ("shipping", "Shipping"),
                            ("drop_shipping", "Dropshipping"),
                            ("deliverable", "Deliverable"),
                            ("else", "Else"),
                        ],
                        default="billing",
                        help_text="E.g. Shipping or billing",
                        max_length=255,
                        verbose_name="name",
                    ),
                ),
                (
                    "loc_name_custom",
                    models.CharField(
                        blank=True,
                        help_text="Other location name. E.g. Basecamp",
                        max_length=255,
                        null=True,
                        verbose_name="other name",
                    ),
                ),
                ("primary", models.BooleanField(default=False)),
                (
                    "notes",
                    models.TextField(
                        blank=True,
                        help_text="Tell us anything we should know when delivering your order.",
                        verbose_name="Instructions",
                    ),
                ),
                (
                    "content_id",
                    models.IntegerField(
                        blank=True, help_text="Linked order primary key.", null=True
                    ),
                ),
                (
                    "content_type",
                    models.ForeignKey(
                        blank=True,
                        help_text="Linked order",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="deliverable_addresses",
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "country",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="coreplus_contacts.country",
                        verbose_name="Country",
                    ),
                ),
            ],
            options={
                "verbose_name": "Deliverable address",
                "verbose_name_plural": "Deliverable addresses",
            },
        ),
        migrations.CreateModel(
            name="BillingAddress",
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
                    "address",
                    models.CharField(max_length=255, null=True, verbose_name="address"),
                ),
                (
                    "city",
                    models.CharField(max_length=255, null=True, verbose_name="city"),
                ),
                (
                    "state",
                    models.CharField(
                        max_length=255, null=True, verbose_name="province"
                    ),
                ),
                (
                    "postcode",
                    coreplus.utils.models.fields.UppercaseCharField(
                        blank=True, max_length=64, verbose_name="Post/Zip-code"
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        choices=[
                            ("Mr", "Mr"),
                            ("Miss", "Miss"),
                            ("Mrs", "Mrs"),
                            ("Ms", "Ms"),
                            ("Dr", "Dr"),
                        ],
                        help_text="Treatment Pronouns for the contact",
                        max_length=64,
                        null=True,
                        verbose_name="Title",
                    ),
                ),
                (
                    "contact",
                    models.CharField(
                        help_text="Contact name will be used.",
                        max_length=255,
                        null=True,
                        verbose_name="contact",
                    ),
                ),
                (
                    "phone",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True,
                        help_text="In case we need to call you about your order",
                        max_length=128,
                        region=None,
                        verbose_name="Phone number",
                    ),
                ),
                (
                    "loc_name",
                    models.CharField(
                        choices=[
                            ("home", "Home"),
                            ("office", "Office"),
                            ("branch_office", "Branch Office"),
                            ("billing", "Billing"),
                            ("shipping", "Shipping"),
                            ("drop_shipping", "Dropshipping"),
                            ("deliverable", "Deliverable"),
                            ("else", "Else"),
                        ],
                        default="billing",
                        help_text="E.g. Shipping or billing",
                        max_length=255,
                        verbose_name="name",
                    ),
                ),
                (
                    "loc_name_custom",
                    models.CharField(
                        blank=True,
                        help_text="Other location name. E.g. Basecamp",
                        max_length=255,
                        null=True,
                        verbose_name="other name",
                    ),
                ),
                ("primary", models.BooleanField(default=False)),
                (
                    "notes",
                    models.TextField(
                        blank=True,
                        help_text="Tell us anything we should know when delivering your order.",
                        verbose_name="Instructions",
                    ),
                ),
                (
                    "content_id",
                    models.IntegerField(
                        blank=True, help_text="Linked order primary key.", null=True
                    ),
                ),
                (
                    "content_type",
                    models.ForeignKey(
                        blank=True,
                        help_text="Linked order",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="billing_addresses",
                        to="contenttypes.contenttype",
                    ),
                ),
                (
                    "country",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="coreplus_contacts.country",
                        verbose_name="Country",
                    ),
                ),
            ],
            options={
                "verbose_name": "Billing address",
                "verbose_name_plural": "Billing addresses",
            },
        ),
    ]
