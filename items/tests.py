from django.contrib.auth.models import User
from django.test import TestCase, Client

from .models import Item, Category

from .utils import *


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


class ProductTests(TestCase):

    fixtures = ['items/load_data.json']

    conduit = Item.objects.filter(title="Кожух").first()
    core = Item.objects.filter(title="Сердечник").first()

    def test_std_cable_creation(self):

        create_std_cable(
            conduit_id=self.conduit.id,
            core_id=self.core.id,
            serie=4,
            travel=3,
            mounting="23",
            is_steel_rods=True,
            is_steel_sleeves=False,
            is_plastic_sleeves=False,
            length=1500)

        cable = Product.objects.all().first()
        self.assertEqual(cable.part_number, "100.M4323.01500")
        self.assertEqual(len(cable.components), 12)

        core = cable.components.filter(item__title="Сердечник").first()
        conduit = cable.components.filter(item__title="Кожух").first()
        self.assertEqual(core.quantity, 1500 - 224 + 15)
        self.assertEqual(conduit.quantity, 1500 - 406 + 15)

    def test_tza_cable_creation(self):

        create_tza_cable(
            conduit_id=self.conduit.id,
            core_id=self.core.id,
            is_steel_rods=True,
            length=7500)

        cable = Product.objects.all().first()

        self.assertEqual(cable.part_number, "ТЗА-100.М4(110)20.07500-01")
        self.assertEqual(len(cable.components), 13)
