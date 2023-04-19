# Generated by Django 4.1.7 on 2023-04-10 21:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_userprofile_wiki_handle_and_more'),
        ('bug', '0002_alter_bug_date_of_report_alter_bug_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bug',
            name='reporter',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, related_name='reporter', to='users.userprofile'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bug',
            name='title',
            field=models.CharField(max_length=140, verbose_name='Title'),
        ),
    ]