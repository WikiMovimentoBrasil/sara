# Generated by Django 4.1.7 on 2024-01-30 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('metrics', '0012_metric_is_operation'),
        ('report', '0030_report_number_of_community_communications_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='number_of_community_communications',
        ),
        migrations.RemoveField(
            model_name='report',
            name='number_of_events',
        ),
        migrations.RemoveField(
            model_name='report',
            name='number_of_mentions',
        ),
        migrations.RemoveField(
            model_name='report',
            name='number_of_new_followers',
        ),
        migrations.RemoveField(
            model_name='report',
            name='number_of_people_reached_through_social_media',
        ),
        migrations.RemoveField(
            model_name='report',
            name='resources',
        ),
        migrations.CreateModel(
            name='OperationReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_people_reached_through_social_media', models.IntegerField(blank=True, default=0)),
                ('number_of_new_followers', models.IntegerField(blank=True, default=0)),
                ('number_of_mentions', models.IntegerField(blank=True, default=0)),
                ('number_of_community_communications', models.IntegerField(blank=True, default=0)),
                ('number_of_events', models.IntegerField(blank=True, default=0)),
                ('resources', models.IntegerField(blank=True, default=0)),
                ('number_of_partnerships', models.IntegerField(blank=True, default=0)),
                ('metric', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='operation_metric', to='metrics.metric')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operation_report', to='report.report')),
            ],
        ),
    ]