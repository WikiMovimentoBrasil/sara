# Generated by Django 4.1.7 on 2023-04-23 10:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0015_alter_report_directions_related'),
    ]

    operations = [
        migrations.DeleteModel(
            name='EvaluationObjectiveAnswer',
        ),
    ]