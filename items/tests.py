from django.test import TestCase

from .models import Item, Category


def create_category(name, notes):
    return Category.objects.create(
        name=name,
        notes=notes)


def create_item(title, part_number, part_number2, picture, category, notes):
    return Item.objects.create(
        title=title,
        part_number=part_number,
        part_number2=part_number2,
        picture=picture,
        category=category,
        notes=notes)


class ItemTests(TestCase):

    def test_category_creation(self):

        category = create_category(
            name="Тестова категорія",
            notes="Тестова нотатка")
        self.assertIs(category.name, "Тестова категорія")
        self.assertIs(category.notes, "Тестова нотатка")

    def test_item_creation(self):

        item = create_item(
            title="Деталь 1",
            part_number="00_123",
            part_number2="",
            picture="",
            category=create_category(
                name="Тестова категорія",
                notes="Тестова нотатка"),
            notes="Тестова нотатка деталі")
        self.assertIs(item.title, "Деталь 1")
        self.assertIs(item.part_number, "00_123")
        self.assertIs(item.category.name, "Тестова категорія")
        self.assertIs(item.category.notes, "Тестова нотатка")
        self.assertIs(item.picture, None)
