# Generated by Django 4.2 on 2023-05-05 14:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("copies", "0003_alter_loan_return_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="loan",
            name="return_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
