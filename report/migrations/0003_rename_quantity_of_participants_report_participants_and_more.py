# Generated by Django 4.1.7 on 2023-03-15 19:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0002_alter_areaactivated_contact'),
    ]

    operations = [
        migrations.RenameField(
            model_name='report',
            old_name='quantity_of_participants',
            new_name='participants',
        ),
        migrations.RemoveField(
            model_name='report',
            name='should_be_on_meta',
        ),
    ]