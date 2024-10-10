import json
from django.core.management.base import BaseCommand
from procedures.models import Procedure

class Command(BaseCommand):
    help = 'Import procedures from a JSON file'

    def handle(self, *args, **kwargs):
        with open('procedures/procedures.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            for item in data:
                # Use float for the cost value directly
                cost = float(item.get('cost', 0))

                Procedure.objects.update_or_create(
                    name=item.get('name', 'Unnamed Procedure'),
                    defaults={
                        'description': item.get('description', 'No description available'),
                        'cost': cost,
                        'duration': item.get('duration', 60),
                        'expiration': item.get('expiration', 365),
                        'region': item.get('region', 'Unknown'),
                        'complaint': item.get('complaint', ''),
                    }
                )
            self.stdout.write(self.style.SUCCESS('Successfully imported procedures'))
