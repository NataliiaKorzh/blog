# Generated by Django 5.0.3 on 2024-06-09 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="is_subscribed",
            field=models.BooleanField(default=False),
        ),
    ]
