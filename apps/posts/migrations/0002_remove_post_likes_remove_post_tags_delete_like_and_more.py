# Generated by Django 4.2.7 on 2023-12-14 14:27

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="likes",
        ),
        migrations.RemoveField(
            model_name="post",
            name="tags",
        ),
        migrations.DeleteModel(
            name="Like",
        ),
        migrations.DeleteModel(
            name="Tag",
        ),
    ]
