# Generated by Django 4.1.7 on 2023-04-27 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_userprofile_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(blank=True, choices=[('1', 'Male'), ('2', 'Female'), ('3', 'Non Binary'), ('4', 'Other'), ('5', 'Not declared')], default='5', max_length=2, null=True),
        ),
    ]