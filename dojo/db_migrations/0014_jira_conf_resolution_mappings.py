# Generated by Django 2.2.3 on 2019-07-24 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dojo', '0013_jira_info_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='jira_conf',
            name='accepted_mapping_resolution',
            field=models.CharField(blank=True, help_text='JIRA resolution names (comma-separated values) that maps to an Accepted Finding', max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='jira_conf',
            name='false_positive_mapping_resolution',
            field=models.CharField(blank=True, help_text='JIRA resolution names (comma-separated values) that maps to a False Positive Finding', max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='jira_conf',
            name='under_review_mapping_resolution',
            field=models.CharField(blank=True, help_text='JIRA resolution names (comma-separated values) that maps to an Under Review Finding', max_length=300, null=True),
        ),
    ]
