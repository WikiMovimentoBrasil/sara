# Generated by Django 4.1.7 on 2023-04-23 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('strategy', '0001_initial'),
        ('report', '0014_alter_report_directions_related'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='directions_related',
            field=models.ManyToManyField(related_name='direction_related', to='strategy.direction'),
        ),
    ]
