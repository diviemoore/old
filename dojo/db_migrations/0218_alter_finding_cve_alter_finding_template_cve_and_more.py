# Generated by Django 4.1.13 on 2024-06-27 13:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dojo", "0217_alter_vulnerability_id_vulnerability_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="finding",
            name="cve",
            field=models.CharField(
                help_text="An id of a vulnerability in a security advisory associated with this finding. Can be a Common Vulnerabilities and Exposures (CVE) or from other sources.",
                max_length=100,
                null=True,
                verbose_name="Vulnerability Id",
            ),
        ),
        migrations.AlterField(
            model_name="finding_template",
            name="cve",
            field=models.CharField(
                help_text="An id of a vulnerability in a security advisory associated with this finding. Can be a Common Vulnerabilities and Exposures (CVE) or from other sources.",
                max_length=100,
                null=True,
                verbose_name="Vulnerability Id",
            ),
        ),
        migrations.AlterField(
            model_name="vulnerability_id_template",
            name="vulnerability_id",
            field=models.TextField(max_length=100),
        ),
    ]
