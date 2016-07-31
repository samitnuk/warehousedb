from django.contrib import admin

from .models import Item, ItemChange

admin.site.register(Item)
admin.site.register(ItemChange)
