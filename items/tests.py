from django.test import TestCase

from .models import Item, Category

class ItemTests(TestCase):

    def test_item_creation(self):

        category = Category.objects.create(
            name="Тестова категорія",
            notes="Тестова нотатка")
        self.assertIs(category.name, "Тестова категорія")
        self.assertIs(category.notes, "Тестова нотатка")

        item = Item.objects.create(
            title="Деталь 1",
            part_number="00_123",
            category=category)
        self.assertIs(item.title, "Деталь 1")
        self.assertIs(item.part_number, "00_123")
        self.assertIs(item.category.name, "Тестова категорія")
        self.assertIs(item.category.notes, "Тестова нотатка")
