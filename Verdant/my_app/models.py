
from django.utils import timezone
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Accessory model
class Accessory(models.Model):
    ACCESSORY_TYPES = [
        ('pot', 'Pot'),
        ('tag', 'Tag'),
        ('decoration', 'Decoration'),
        ('tool', 'Tool'),
        ('fertilizer', 'Fertilizer'),
    ]

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=ACCESSORY_TYPES)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.type})"

    def get_absolute_url(self):
        return reverse("accessory-detail", kwargs={"pk": self.id})

# Plant model
class Plant(models.Model):
    GROWTH_STAGES = [
        ('healthy', 'Healthy'),
        ('unhealthy', 'Unhealthy'),
        ('weak', 'Weak'),
        ('dying', 'Dying'),
        ('dead', 'Dead'),
    ]

    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    planting_date = models.DateField(auto_now_add=True)
    growth_stage = models.CharField(  # <-- keep this name
        max_length=20,
        choices=GROWTH_STAGES,
        default='healthy'
    )
    health = models.IntegerField(default=100)
    last_cared_for = models.DateTimeField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plants')
    accessories = models.ManyToManyField(Accessory, blank=True, related_name='plants')

    def __str__(self):
        return f"{self.name} ({self.species})"

    def get_absolute_url(self):
        return reverse("plant-detail", kwargs={"pk": self.id})

    def save(self, *args, **kwargs):
        """Automatically update growth_stage based on health each time the plant is saved."""
        if self.health <= 0:
            self.growth_stage = 'dead'
        elif self.health <= 20:
            self.growth_stage = 'wilting'
        elif self.health <= 40:
            self.growth_stage = 'weak'
        elif self.health <= 70:
            self.growth_stage = 'unhealthy'
        else:
            self.growth_stage = 'healthy'

        super().save(*args, **kwargs)


    @property
    def is_dead(self):
        return self.health <= 0
    
    @property
    def needs_watering(self):
        return self._needs_care('water', hours=0.5)

    @property
    def needs_fertilizer(self):
        return self._needs_care('fertilize', hours=0.5)

    @property
    def needs_pruning(self):
        return self._needs_care('prune', hours=0.5)

    @property
    def needs_sunlight(self):
        return self._needs_care('sunlight', hours=0.5)

    def _needs_care(self, action_type, hours):
        last_action = self.care_actions.filter(action_type=action_type).order_by('-date').first()
        if not last_action:
            return True  # never done → needs care
        hours_passed = (timezone.now() - last_action.date).total_seconds() / 3600
        return hours_passed >= hours

# CareAction model

class CareAction(models.Model):
    ACTION_TYPES = [
        ('water', 'Watering'),
        ('fertilize', 'Fertilizing'),
        ('prune', 'Pruning'),
        ('sunlight', 'Sunlight Adjustment'),
    ]

    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='care_actions')
    action_type = models.CharField(max_length=20, choices=ACTION_TYPES)
    date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.action_type} on {self.plant.name} ({self.date.date()})"

    def save(self, *args, **kwargs):
        plant = self.plant

        if plant.is_dead:
            super().save(*args, **kwargs)
            return

        # Capture needs BEFORE saving this action
        needs_before = {
            'water': plant.needs_watering,
            'fertilize': plant.needs_fertilizer,
            'prune': plant.needs_pruning,
            'sunlight': plant.needs_sunlight,
        }

        super().save(*args, **kwargs)  # save the CareAction

        # Apply HP changes based on needs BEFORE this action
        if needs_before.get(self.action_type, False):
            plant.health = min(100, plant.health + 20)  # correct care
            message = f"{self.action_type.capitalize()} done on {plant.name}."
        else:
            plant.health = max(0, plant.health - 5)    # wrong care
            message = f"{self.action_type.capitalize()} incorrectly done on {plant.name}!"

        plant.last_cared_for = timezone.now()
        plant.save()

        # Create a PlantActivity entry
        PlantActivity.objects.create(plant=plant, message=message, timestamp=timezone.now())

    @property
    def last_action_time(self):
        last_action = self.care_actions.order_by('-date').first()
        if last_action:
            return last_action.date
        return None
    
class PlantActivity(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
