# Generated by Django 4.1.7 on 2023-05-04 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metrics', '0004_project_status_alter_metric_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='project',
            field=models.ManyToManyField(blank=True, related_name='project_activity', to='metrics.project'),
        ),
    ]
