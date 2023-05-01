# Generated by Django 4.1.7 on 2023-04-23 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('strategy', '0001_initial'),
        ('report', '0013_alter_report_public_communication'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='directions_related',
            field=models.ManyToManyField(limit_choices_to={'direction_related__lt': 3}, related_name='direction_related', to='strategy.direction'),
        ),
    ]