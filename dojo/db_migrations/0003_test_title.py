# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-23 09:34


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dojo", "0002_auto_20190503_1817"),
    ]

    operations = [
        migrations.AddField(
            model_name="test",
            name="title",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
