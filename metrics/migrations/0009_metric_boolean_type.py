# Generated by Django 4.1.7 on 2023-10-20 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metrics', '0008_metric_number_of_organizers_retained_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='metric',
            name='boolean_type',
            field=models.BooleanField(default=False),
        ),
    ]