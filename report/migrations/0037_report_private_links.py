# Generated by Django 5.1.1 on 2024-11-20 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0036_report_reference_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='private_links',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]