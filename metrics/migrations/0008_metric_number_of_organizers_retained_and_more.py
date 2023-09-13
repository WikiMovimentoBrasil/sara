# Generated by Django 4.1.7 on 2023-09-12 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metrics', '0007_metric_number_of_new_editors'),
    ]

    operations = [
        migrations.AddField(
            model_name='metric',
            name='number_of_organizers_retained',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='metric',
            name='number_of_people_reached_through_social_media',
            field=models.IntegerField(default=0, null=True),
        ),
    ]