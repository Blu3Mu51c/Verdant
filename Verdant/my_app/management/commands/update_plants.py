from django.core.management.base import BaseCommand
from django.utils import timezone
from my_app.models import Plant
from datetime import timedelta

class Command(BaseCommand):
    help = "Update plant health and growth automatically"

    def handle(self, *args, **kwargs):
        now = timezone.now()
        for plant in Plant.objects.all():
            hours_since_care = (now - plant.last_cared_for).total_seconds() / 3600

            # Health decay if neglected
            if hours_since_care > 24:
                plant.health = max(0, plant.health - 5)

            # Growth progression (simple example)
            if plant.health >= 80:
                stages = ['seedling', 'juvenile', 'mature', 'flowering']
                idx = stages.index(plant.growth_stage)
                if idx + 1 < len(stages):
                    plant.growth_stage = stages[idx + 1]

            plant.save()

        self.stdout.write(self.style.SUCCESS("Plants updated successfully!"))
