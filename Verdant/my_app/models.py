from django.db import models
from django.contrib.auth.models import User


# Accessories that can be attached to plants
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


# Main Plant model
class Plant(models.Model):
    GROWTH_STAGES = [
        ('seedling', 'Seedling'),
        ('juvenile', 'Juvenile'),
        ('mature', 'Mature'),
        ('flowering', 'Flowering'),
    ]

    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    planting_date = models.DateField(auto_now_add=True)
    growth_stage = models.CharField(max_length=20, choices=GROWTH_STAGES, default='seedling')
    health = models.IntegerField(default=100)
    last_cared_for = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plants')
    accessories = models.ManyToManyField(Accessory, blank=True, related_name='plants')

    def __str__(self):
        return f"{self.name} ({self.species})"


# Tracks user interactions with plants
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
