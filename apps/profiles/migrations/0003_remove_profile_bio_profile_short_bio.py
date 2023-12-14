# Generated by Django 4.2.7 on 2023-12-14 11:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("profiles", "0002_alter_profile_options"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="bio",
        ),
        migrations.AddField(
            model_name="profile",
            name="short_bio",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
