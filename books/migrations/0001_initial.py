# Generated by Django 4.2 on 2023-05-01 20:08

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Book",
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
                ("title", models.CharField(max_length=200, unique=True)),
                ("author", models.CharField(max_length=100)),
                ("category", models.CharField(max_length=50)),
                ("summary", models.TextField(null=True)),
            ],
        ),
    ]
