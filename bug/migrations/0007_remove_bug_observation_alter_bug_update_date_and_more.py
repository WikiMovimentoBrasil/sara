# Generated by Django 4.1.7 on 2023-04-18 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bug', '0006_alter_bug_reporter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bug',
            name='observation',
        ),
        migrations.AlterField(
            model_name='bug',
            name='update_date',
            field=models.DateField(auto_now=True, verbose_name='Update date'),
        ),
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observation', models.TextField(max_length=500, verbose_name='Observation')),
                ('date_of_answer', models.DateTimeField(auto_now_add=True)),
                ('bug_report', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='observation', to='bug.bug')),
            ],
        ),
    ]
