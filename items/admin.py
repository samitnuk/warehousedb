from django.contrib import admin

import items.models as models

admin.site.register(models.Item)
admin.site.register(models.ItemChange)
admin.site.register(models.Category)
admin.site.register(models.Order)
admin.site.register(models.Product)
admin.site.register(models.OrderLine)
admin.site.register(models.Component)
