# Generated by Django 2.2.12 on 2020-05-04 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dojo', '0041_engagement_survey_import'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finding',
            name='hash_code',
            field=models.CharField(blank=True, editable=False, max_length=64, null=True),
        ),
        migrations.AddIndex(
            model_name='finding',
            index=models.Index(fields=['hash_code'], name='dojo_findin_hash_co_09df6a_idx'),
        ),
        migrations.AddIndex(
            model_name='finding',
            index=models.Index(fields=['unique_id_from_tool'], name='dojo_findin_unique__f76d47_idx'),
        ),
        migrations.AddIndex(
            model_name='finding',
            index=models.Index(fields=['line'], name='dojo_findin_line_fea329_idx'),
        ),
    ]
