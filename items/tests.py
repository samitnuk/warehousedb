from django.contrib.auth.models import User
from django.test import TestCase, Client

from .models import Item, Category


def create_user(username, password):
    return User.objects.create(
        username=username,
        password=password)


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


class UserTests(TestCase):

    def test_user_creation(self):

        user = create_user('test_user', 'test_password')
        self.assertEqual(user.username, 'test_user')


class LoginTests(TestCase):

    def test_login(self):

        create_user('test_user', 'test_password')
        c = Client()
        responce = c.post(
            '/login/',
            {'username': 'test_user', 'password': 'test_password'})
        self.assertEqual(responce.status_code, 200)


class ItemTests(TestCase):

    def test_category_creation(self):

        category = create_category(
            name="Тестова категорія",
            notes="Тестова нотатка")
        self.assertEqual(category.name, "Тестова категорія")
        self.assertEqual(category.notes, "Тестова нотатка")

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
        self.assertEqual(item.title, "Деталь 1")
        self.assertEqual(item.part_number, "00_123")
        self.assertEqual(item.category.name, "Тестова категорія")
        self.assertEqual(item.category.notes, "Тестова нотатка")
        # self.assertEqual(item.picture, None)
