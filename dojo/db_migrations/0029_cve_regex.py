# Generated by Django 2.2.10 on 2020-02-20 20:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dojo", "0028_finding_indices"),
    ]

    operations = [
        migrations.AlterField(
            model_name="finding",
            name="cve",
            field=models.CharField(
                help_text="CVE or other vulnerability identifier",
                max_length=28,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Vulnerability ID must be entered in the format: 'ABC-9999-9999'.",
                        regex="^[A-Z]{1,10}(-\\d+)+$",
                    )
                ],
            ),
        ),
        migrations.AlterField(
            model_name="finding_template",
            name="cve",
            field=models.CharField(
                max_length=28,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Vulnerability ID must be entered in the format: 'ABC-9999-9999'.",
                        regex="^[A-Z]{1,10}(-\\d+)+$",
                    )
                ],
            ),
        ),
    ]
