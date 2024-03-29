# Generated by Django 4.1.7 on 2024-02-19 03:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_teamarea_color_code'),
        ('metrics', '0013_activity_is_main_activity'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='area_responsible',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='activity_manager', to='users.teamarea'),
        ),
    ]
