from django.contrib import admin

from .models import Item, ItemChange, Category

admin.site.register(Item)
admin.site.register(ItemChange)
admin.site.register(Category)
