# Generated by Django 2.2.12 on 2020-05-08 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dojo", "0052_cvssv3_field"),
    ]

    operations = [
        migrations.AddField(
            model_name="engagement",
            name="notes",
            field=models.ManyToManyField(blank=True, editable=False, to="dojo.Notes"),
        ),
    ]
