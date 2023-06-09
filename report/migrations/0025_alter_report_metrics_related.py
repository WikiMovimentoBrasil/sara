# Generated by Django 4.1.7 on 2023-06-28 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metrics', '0005_area_project'),
        ('report', '0024_alter_report_metrics_related'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='metrics_related',
            field=models.ManyToManyField(related_name='metrics_related', to='metrics.metric'),
        ),
    ]
