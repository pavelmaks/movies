# Generated by Django 4.2.1 on 2023-08-28 14:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_filmwork_person_alter_filmwork_certificate_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filmwork',
            name='certificate',
        ),
        migrations.RemoveField(
            model_name='filmwork',
            name='file_path',
        ),
        migrations.RemoveField(
            model_name='person',
            name='gender',
        ),
    ]
