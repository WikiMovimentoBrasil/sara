# Generated by Django 4.1.7 on 2023-03-18 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bug', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bug',
            name='date_of_report',
            field=models.DateField(auto_now_add=True, verbose_name='Date of report'),
        ),
        migrations.AlterField(
            model_name='bug',
            name='description',
            field=models.TextField(max_length=500, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='bug',
            name='observation',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='Observation'),
        ),
        migrations.AlterField(
            model_name='bug',
            name='status',
            field=models.CharField(choices=[('1', 'To do'), ('2', 'In progress'), ('3', 'Testing'), ('4', 'Done')], default='1', max_length=1, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='bug',
            name='title',
            field=models.CharField(blank=True, max_length=140, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='bug',
            name='type_of_bug',
            field=models.CharField(choices=[('1', 'Error'), ('2', 'Improvement request'), ('3', 'New feature request'), ('4', 'Question or clarification')], default='1', max_length=1, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='bug',
            name='update_date',
            field=models.DateField(null=True, verbose_name='Update date'),
        ),
    ]
