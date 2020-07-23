from django.core.management.base import BaseCommand
from django.db.models import Count
from dojo.models import Endpoint, Finding, Endpoint_Status


"""
Author: Cody Maffucci
This script will create endpoint status objects for findings and endpoints for
databases that already contain those objects. This script should only be run when 
upgrading to 1.7.0 as it is unnecessary for fresh installs
"""


class Command(BaseCommand):
    help = 'Create status objects for Endpoints for easier tracking'

    def handle(self, *args, **options):
        # Get a list of findings that have endpoints
        findings = Finding.objects.annotate(count=Count('endpoints')).filter(count__gt=0)
        for finding in findings:
            # Get the list of endpoints on the current finding
            endpoints = finding.endpoints.all()
            for endpoint in endpoints:
                # Create a new status for each endpoint
                status = Endpoint_Status.objects.create(
                    finding=finding,
                    endpoint=endpoint,
                    date=finding.date,
                    )
                # If the endpoint was mitigated in the older fashion, update the status to reflect that
                if endpoint.mitigated:
                    status.mitigated = True
                    status.mitigated_by = finding.reporter
                    status.save()
                # Attach the status to the endpoint and finding
                endpoint.endpoint_status.add(status)
                finding.endpoint_status.add(status)
