from django.core.management.base import BaseCommand
from my_app.models import Plant

class Command(BaseCommand):
    help = "Decays plant health if not watered/fertilized/etc."
    
    def handle(self, *args, **kwargs):
        for plant in Plant.objects.all():
            
            if plant.needs_watering:
                plant.health = max(0, plant.health - 10)
            if plant.needs_fertilizer:
                plant.health = max(0, plant.health - 5)
            if plant.needs_pruning:
                plant.health = max(0, plant.health - 5)
            if plant.needs_sunlight:
                plant.health = max(0, plant.health - 5)
            plant.save()
