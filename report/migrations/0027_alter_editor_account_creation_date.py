# Generated by Django 4.1.7 on 2023-07-17 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0026_editor_account_creation_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='editor',
            name='account_creation_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
