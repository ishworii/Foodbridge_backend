# Generated by Django 5.2.3 on 2025-06-29 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_profile"),
    ]

    operations = [
        migrations.AddField(
            model_name="donation",
            name="expiry_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="donation",
            name="food_type",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="donation",
            name="latitude",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="donation",
            name="longitude",
            field=models.FloatField(blank=True, null=True),
        ),
    ]
