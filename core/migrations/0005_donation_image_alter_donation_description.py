# Generated by Django 5.2.3 on 2025-06-30 00:26

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_donation_expiry_date_donation_food_type_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="donation",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="donations/"),
        ),
        migrations.AlterField(
            model_name="donation",
            name="description",
            field=ckeditor.fields.RichTextField(),
        ),
    ]
