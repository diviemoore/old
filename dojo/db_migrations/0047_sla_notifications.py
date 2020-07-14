# Generated by Django 2.2.14 on 2020-07-10 09:34

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dojo', '0046_endpoint_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='jira_conf',
            name='sla_notification',
            field=models.BooleanField(default=True, verbose_name='Globally send SLA notifications as comment?', help_text="This setting can be overidden at the Product level"),
        ),
        migrations.AddField(
            model_name='notifications',
            name='sla_breach',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('slack', 'slack'), ('hipchat', 'hipchat'), ('mail', 'mail'), ('alert', 'alert')], default='alert', help_text='Get notified of upcoming SLA breaches', max_length=24, verbose_name='SLA breach'),
        ),
        migrations.AddField(
            model_name='jira_pkey',
            name='sla_notification',
            field=models.BooleanField(default=True, verbose_name='Send SLA notifications as comment?'),
        ),
    ]
