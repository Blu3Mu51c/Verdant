from django.contrib import admin
from .models import Plant, Accessory, CareAction

@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'growth_stage', 'health', 'owner')
    list_filter = ('growth_stage', 'species')
    search_fields = ('name', 'species')

@admin.register(Accessory)
class AccessoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')
    list_filter = ('type',)
    search_fields = ('name',)

@admin.register(CareAction)
class CareActionAdmin(admin.ModelAdmin):
    list_display = ('plant', 'action_type', 'date')
    list_filter = ('action_type', 'date')
    search_fields = ('plant__name', 'action_type')
