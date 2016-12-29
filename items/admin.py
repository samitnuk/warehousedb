from django.contrib import admin
from django.core.urlresolvers import reverse

import items.models as models


class ItemAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'part_number', 'part_number2', 'category', 'notes']
    ordering = ['title']
    list_filter = ['category']
    list_per_page = 50

    def view_on_site(self, obj):
        return reverse('item_detail', kwargs={'pk': obj.id})

admin.site.register(models.Item, ItemAdmin)
admin.site.register(models.ItemChange)
admin.site.register(models.Category)
admin.site.register(models.Order)
admin.site.register(models.Product)
admin.site.register(models.Component)
