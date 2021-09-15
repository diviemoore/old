from django.core.management.base import BaseCommand
from dojo.tools.factory import PARSERS


class Command(BaseCommand):
    help = 'Initializes Test_Types'

    def handle(self, *args, **options):
        # called by the initializer to fill the table with test_types
        for scan_type in PARSERS:
            test_type, created = Test_Type.objects.get_or_create(name=scan_type)
            if created:
                test_type.save()
