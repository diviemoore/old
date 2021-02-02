# Generated by Django 2.2.12 on 2020-04-14 19:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dojo", "0051_regulation_categories"),
    ]

    operations = [
        migrations.AddField(
            model_name="finding",
            name="cvssv3",
            field=models.TextField(
                max_length=117,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="CVSS must be entered in format: 'AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H'",
                        regex="^AV:[NALP]|AC:[LH]|PR:[UNLH]|UI:[NR]|S:[UC]|[CIA]:[NLH]",
                    )
                ],
            ),
        ),
        migrations.AddField(
            model_name="finding_template",
            name="cvssv3",
            field=models.TextField(
                max_length=117,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="CVSS must be entered in format: 'AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H'",
                        regex="^AV:[NALP]|AC:[LH]|PR:[UNLH]|UI:[NR]|S:[UC]|[CIA]:[NLH]",
                    )
                ],
            ),
        ),
        migrations.AlterField(
            model_name="child_rule",
            name="match_field",
            field=models.CharField(
                choices=[
                    ("id", "id"),
                    ("title", "title"),
                    ("date", "date"),
                    ("cwe", "cwe"),
                    ("cve", "cve"),
                    ("cvssv3", "cvssv3"),
                    ("url", "url"),
                    ("severity", "severity"),
                    ("description", "description"),
                    ("mitigation", "mitigation"),
                    ("impact", "impact"),
                    ("steps_to_reproduce", "steps_to_reproduce"),
                    ("severity_justification", "severity_justification"),
                    ("references", "references"),
                    ("test", "test"),
                    ("is_template", "is_template"),
                    ("active", "active"),
                    ("verified", "verified"),
                    ("false_p", "false_p"),
                    ("duplicate", "duplicate"),
                    ("duplicate_finding", "duplicate_finding"),
                    ("out_of_scope", "out_of_scope"),
                    ("under_review", "under_review"),
                    ("review_requested_by", "review_requested_by"),
                    ("under_defect_review", "under_defect_review"),
                    ("defect_review_requested_by", "defect_review_requested_by"),
                    ("is_Mitigated", "is_Mitigated"),
                    ("thread_id", "thread_id"),
                    ("mitigated", "mitigated"),
                    ("mitigated_by", "mitigated_by"),
                    ("reporter", "reporter"),
                    ("numerical_severity", "numerical_severity"),
                    ("last_reviewed", "last_reviewed"),
                    ("last_reviewed_by", "last_reviewed_by"),
                    ("line_number", "line_number"),
                    ("sourcefilepath", "sourcefilepath"),
                    ("sourcefile", "sourcefile"),
                    ("param", "param"),
                    ("payload", "payload"),
                    ("hash_code", "hash_code"),
                    ("line", "line"),
                    ("file_path", "file_path"),
                    ("component_name", "component_name"),
                    ("component_version", "component_version"),
                    ("static_finding", "static_finding"),
                    ("dynamic_finding", "dynamic_finding"),
                    ("created", "created"),
                    ("jira_creation", "jira_creation"),
                    ("jira_change", "jira_change"),
                    ("scanner_confidence", "scanner_confidence"),
                    ("sonarqube_issue", "sonarqube_issue"),
                    ("unique_id_from_tool", "unique_id_from_tool"),
                    ("sast_source_object", "sast_source_object"),
                    ("sast_sink_object", "sast_sink_object"),
                    ("sast_source_line", "sast_source_line"),
                    ("sast_source_file_path", "sast_source_file_path"),
                    ("nb_occurences", "nb_occurences"),
                ],
                max_length=200,
            ),
        ),
        migrations.AlterField(
            model_name="rule",
            name="applied_field",
            field=models.CharField(
                choices=[
                    ("id", "id"),
                    ("title", "title"),
                    ("date", "date"),
                    ("cwe", "cwe"),
                    ("cve", "cve"),
                    ("cvssv3", "cvssv3"),
                    ("url", "url"),
                    ("severity", "severity"),
                    ("description", "description"),
                    ("mitigation", "mitigation"),
                    ("impact", "impact"),
                    ("steps_to_reproduce", "steps_to_reproduce"),
                    ("severity_justification", "severity_justification"),
                    ("references", "references"),
                    ("test", "test"),
                    ("is_template", "is_template"),
                    ("active", "active"),
                    ("verified", "verified"),
                    ("false_p", "false_p"),
                    ("duplicate", "duplicate"),
                    ("duplicate_finding", "duplicate_finding"),
                    ("out_of_scope", "out_of_scope"),
                    ("under_review", "under_review"),
                    ("review_requested_by", "review_requested_by"),
                    ("under_defect_review", "under_defect_review"),
                    ("defect_review_requested_by", "defect_review_requested_by"),
                    ("is_Mitigated", "is_Mitigated"),
                    ("thread_id", "thread_id"),
                    ("mitigated", "mitigated"),
                    ("mitigated_by", "mitigated_by"),
                    ("reporter", "reporter"),
                    ("numerical_severity", "numerical_severity"),
                    ("last_reviewed", "last_reviewed"),
                    ("last_reviewed_by", "last_reviewed_by"),
                    ("line_number", "line_number"),
                    ("sourcefilepath", "sourcefilepath"),
                    ("sourcefile", "sourcefile"),
                    ("param", "param"),
                    ("payload", "payload"),
                    ("hash_code", "hash_code"),
                    ("line", "line"),
                    ("file_path", "file_path"),
                    ("component_name", "component_name"),
                    ("component_version", "component_version"),
                    ("static_finding", "static_finding"),
                    ("dynamic_finding", "dynamic_finding"),
                    ("created", "created"),
                    ("jira_creation", "jira_creation"),
                    ("jira_change", "jira_change"),
                    ("scanner_confidence", "scanner_confidence"),
                    ("sonarqube_issue", "sonarqube_issue"),
                    ("unique_id_from_tool", "unique_id_from_tool"),
                    ("sast_source_object", "sast_source_object"),
                    ("sast_sink_object", "sast_sink_object"),
                    ("sast_source_line", "sast_source_line"),
                    ("sast_source_file_path", "sast_source_file_path"),
                    ("nb_occurences", "nb_occurences"),
                ],
                max_length=200,
            ),
        ),
        migrations.AlterField(
            model_name="rule",
            name="match_field",
            field=models.CharField(
                choices=[
                    ("id", "id"),
                    ("title", "title"),
                    ("date", "date"),
                    ("cwe", "cwe"),
                    ("cve", "cve"),
                    ("cvssv3", "cvssv3"),
                    ("url", "url"),
                    ("severity", "severity"),
                    ("description", "description"),
                    ("mitigation", "mitigation"),
                    ("impact", "impact"),
                    ("steps_to_reproduce", "steps_to_reproduce"),
                    ("severity_justification", "severity_justification"),
                    ("references", "references"),
                    ("test", "test"),
                    ("is_template", "is_template"),
                    ("active", "active"),
                    ("verified", "verified"),
                    ("false_p", "false_p"),
                    ("duplicate", "duplicate"),
                    ("duplicate_finding", "duplicate_finding"),
                    ("out_of_scope", "out_of_scope"),
                    ("under_review", "under_review"),
                    ("review_requested_by", "review_requested_by"),
                    ("under_defect_review", "under_defect_review"),
                    ("defect_review_requested_by", "defect_review_requested_by"),
                    ("is_Mitigated", "is_Mitigated"),
                    ("thread_id", "thread_id"),
                    ("mitigated", "mitigated"),
                    ("mitigated_by", "mitigated_by"),
                    ("reporter", "reporter"),
                    ("numerical_severity", "numerical_severity"),
                    ("last_reviewed", "last_reviewed"),
                    ("last_reviewed_by", "last_reviewed_by"),
                    ("line_number", "line_number"),
                    ("sourcefilepath", "sourcefilepath"),
                    ("sourcefile", "sourcefile"),
                    ("param", "param"),
                    ("payload", "payload"),
                    ("hash_code", "hash_code"),
                    ("line", "line"),
                    ("file_path", "file_path"),
                    ("component_name", "component_name"),
                    ("component_version", "component_version"),
                    ("static_finding", "static_finding"),
                    ("dynamic_finding", "dynamic_finding"),
                    ("created", "created"),
                    ("jira_creation", "jira_creation"),
                    ("jira_change", "jira_change"),
                    ("scanner_confidence", "scanner_confidence"),
                    ("sonarqube_issue", "sonarqube_issue"),
                    ("unique_id_from_tool", "unique_id_from_tool"),
                    ("sast_source_object", "sast_source_object"),
                    ("sast_sink_object", "sast_sink_object"),
                    ("sast_source_line", "sast_source_line"),
                    ("sast_source_file_path", "sast_source_file_path"),
                    ("nb_occurences", "nb_occurences"),
                ],
                max_length=200,
            ),
        ),
    ]
