from django.contrib import admin
from .models import Plant, Accessory, CareAction

# Register your models with the Django admin site
admin.site.register(Plant)
admin.site.register(Accessory)
admin.site.register(CareAction)
