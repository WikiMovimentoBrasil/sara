# Generated by Django 4.1.7 on 2023-03-13 06:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='wiki_handle',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='personal_wiki_handle',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Wiki username'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='photograph',
            field=models.CharField(blank=True, max_length=420, null=True, verbose_name='Photograph'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='professional_wiki_handle',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='WMB username'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='wikidata_item',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=420)),
                ('area_associated', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.teamarea')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
            ],
            options={
                'verbose_name': 'Position',
                'verbose_name_plural': 'Positions',
            },
        ),
    ]
