# Generated by Django 4.1.7 on 2023-04-18 04:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_userprofile_wiki_handle_and_more'),
        ('bug', '0005_alter_bug_reporter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bug',
            name='reporter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='reporter', to='users.userprofile'),
        ),
    ]
