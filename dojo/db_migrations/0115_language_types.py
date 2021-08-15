# Generated by Django 3.1.11 on 2021-06-01 18:04

from django.core.management import call_command
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dojo', '0114_cyclonedx_vuln_uniqu'),
    ]

    def populate_language_types(apps, schema_editor):
        call_command('loaddata', 'language_type')

    operations = [
        # Upload the enhanced list of language types
        migrations.RunPython(populate_language_types),
    ]
