# Generated by Django 2.2.16 on 2020-11-07 11:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("dojo", "0062_add_vuln_id_from_tool"),
    ]

    operations = [
        migrations.DeleteModel(
            name="JIRA_Clone",
        ),
        migrations.DeleteModel(
            name="JIRA_Details_Cache",
        ),
        migrations.RenameModel(
            old_name="JIRA_PKey",
            new_name="JIRA_Project",
        ),
        migrations.AddField(
            model_name="jira_issue",
            name="jira_change",
            field=models.DateTimeField(
                help_text="The date the linked Jira issue was last modified.",
                null=True,
                verbose_name="Jira last update",
            ),
        ),
        migrations.AddField(
            model_name="jira_issue",
            name="jira_creation",
            field=models.DateTimeField(
                help_text="The date a Jira issue was created from this finding.",
                null=True,
                verbose_name="Jira creation",
            ),
        ),
        migrations.RenameModel(
            old_name="JIRA_Conf",
            new_name="JIRA_Instance",
        ),
        migrations.RenameField(
            model_name="jira_project",
            old_name="conf",
            new_name="jira_instance",
        ),
        migrations.AddField(
            model_name="jira_issue",
            name="jira_project",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="dojo.JIRA_Project",
            ),
        ),
        migrations.AddField(
            model_name="JIRA_Project",
            name="engagement",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="dojo.Engagement",
            ),
        ),
        migrations.AlterField(
            model_name="JIRA_Project",
            name="product",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="dojo.Product",
            ),
        ),
        migrations.AlterField(
            model_name="jira_project",
            name="jira_instance",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="dojo.JIRA_Instance",
                verbose_name="JIRA Instance",
            ),
        ),
    ]
