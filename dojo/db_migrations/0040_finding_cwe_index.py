# Generated by Django 2.2.12 on 2020-05-04 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dojo', '0040_finding_cwe_index'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='finding',
            index=models.Index(fields=['cwe'], name='dojo_findin_cwe_a8da22_idx'),
        ),
    ]
