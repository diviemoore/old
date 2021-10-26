# Generated by Django 3.1.13 on 2021-10-07 22:46

from django.db import migrations

from dojo.models import Sonarqube_Product, Cobaltio_Product, Product_API_Scan_Configuration, Test


def migrate_sonarqube(apps, schema_editor):
    sq_products = Sonarqube_Product.objects.all()
    for sq_product in sq_products:
        api_scan_configuration = Product_API_Scan_Configuration()
        api_scan_configuration.product = sq_product.product
        api_scan_configuration.tool_configuration = sq_product.sonarqube_tool_config
        api_scan_configuration.service_key_1 = sq_product.sonarqube_project_key
        api_scan_configuration.save()
        tests = Test.objects.filter(sonarqube_config=sq_product)
        for test in tests:
            test.api_scan_configuration = api_scan_configuration
            test.sonarqube_config = None
            test.save()
        sq_product.delete()


def migrate_cobalt_io(apps, schema_editor):
    cobalt_products = Cobaltio_Product.objects.all()
    for cobalt_product in cobalt_products:
        api_scan_configuration = Product_API_Scan_Configuration()
        api_scan_configuration.product = cobalt_product.product
        api_scan_configuration.tool_configuration = cobalt_product.cobaltio_tool_config
        api_scan_configuration.service_key_1 = cobalt_product.cobaltio_asset_id
        api_scan_configuration.service_key_2 = cobalt_product.cobaltio_asset_name
        api_scan_configuration.save()
        tests = Test.objects.filter(cobaltio_config=cobalt_product)
        for test in tests:
            test.api_scan_configuration = api_scan_configuration
            test.cobaltio_config = None
            test.save()
        cobalt_product.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('dojo', '0130_product_api_scan_configuration'),
    ]

    operations = [
        migrations.RunPython(migrate_sonarqube),
        migrations.RunPython(migrate_cobalt_io),
    ]
