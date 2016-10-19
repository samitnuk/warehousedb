from django.contrib.auth.models import User
from django.test import Client, TestCase

from .models import Category, Item, ItemChange, Order

from .utils import *


def create_user(username, password):
    return User.objects.create(
        username=username,
        password=password)


def create_category(title, notes):
    return Category.objects.create(
        title=title,
        notes=notes)


def create_item(
    title, part_number, part_number2, picture, category, rate, weight, notes
):
    return Item.objects.create(
        title=title,
        part_number=part_number,
        part_number2=part_number2,
        picture=picture,
        category=category,
        rate=rate,
        weight=weight,
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
            title="Тестова категорія",
            notes="Тестова нотатка")
        self.assertEqual(category.title, "Тестова категорія")
        self.assertEqual(category.notes, "Тестова нотатка")

    def test_item_creation(self):

        item = create_item(
            title="Деталь 1",
            part_number="00_123",
            part_number2="",
            picture="",
            category=create_category(
                title="Тестова категорія",
                notes="Тестова нотатка"),
            rate=0,
            weight=0,
            notes="Тестова нотатка деталі")
        self.assertEqual(item.title, "Деталь 1")
        self.assertEqual(item.part_number, "00_123")
        self.assertEqual(item.category.title, "Тестова категорія")
        self.assertEqual(item.category.notes, "Тестова нотатка")
        # self.assertEqual(item.picture, None)


class ItemChangeTests(TestCase):

    fixtures = ['items/load_data.json']

    item = Item.objects.first()

    def test_itemchange_auto_creation(self):

        product = Product.objects.create(
            title="Test PRODUCT",
            part_number="",
            notes="")

        Component.objects.create(
            product=product,
            item=self.item,
            quantity=10)

        Order.objects.create(
            customer="Test ORDER",
            product=product,
            quantity=10)

        itemchanges = ItemChange.objects.all()
        self.assertEqual(len(itemchanges), 0)

        Order.objects.first().delete()

        Order.objects.create(
            customer="Test ORDER",
            product=product,
            quantity=10,
            ready=True)

        itemchanges = ItemChange.objects.all()
        self.assertEqual(len(itemchanges), 1)


class ProductTests(TestCase):

    fixtures = ['items/load_data.json']

    conduit = Item.objects.filter(title="Кожух").first()
    core = Item.objects.filter(title="Сердечник").first()

    length = 2.500   # random number

    def test_std_cable_creation(self):

        create_std_cable(
            conduit_id=self.conduit.id,
            core_id=self.core.id,
            serie=4,
            travel=3,
            mounting="23",
            is_st_rods=True,
            is_st_sleeves=False,
            is_plastic_sleeves=False,
            length=int(self.length * 1000))

        cable = Product.objects.all().first()
        self.assertEqual(cable.part_number, "100.M4323.02500")
        self.assertEqual(len(cable.components), 12)

        core = cable.components.filter(item__title="Сердечник").first()
        conduit = cable.components.filter(item__title="Кожух").first()
        self.assertEqual(core.quantity, self.length - 0.209)
        self.assertEqual(conduit.quantity, self.length - 0.391)

    def test_tza_cable_creation(self):

        create_tza_cable(
            conduit_id=self.conduit.id,
            core_id=self.core.id,
            is_st_rods=True,
            length=int(self.length * 1000))

        cable = Product.objects.all().first()

        self.assertEqual(cable.part_number, "ТЗА-100.М4(110)20.02500-01")
        self.assertEqual(len(cable.components), 13)

        core = cable.components.filter(item__title="Сердечник").first()
        conduit = cable.components.filter(item__title="Кожух").first()
        self.assertEqual(core.quantity, self.length - 0.274)
        self.assertEqual(conduit.quantity, self.length - 0.433)

    def test_H4_cable_creation(self):

        create_H4_cable(
            core_id=self.core.id,
            conduit_id=self.conduit.id,
            is_st_rod_E=False,
            length=int(self.length * 1000))

        cable = Product.objects.all().first()

        self.assertEqual(cable.part_number, "100.М4(40)Г4.02500")
        self.assertEqual(len(cable.components), 14)

        core = cable.components.filter(item__title="Сердечник").first()
        conduit = cable.components.filter(item__title="Кожух").first()
        self.assertEqual(core.quantity, self.length - 0.067)
        self.assertEqual(conduit.quantity, self.length - 0.174)

    def test_H2_cable_creation(self):

        create_H2_cable(
            core_id=self.core.id,
            conduit_id=self.conduit.id,
            is_st_rod_E=True,
            with_01=False,
            length=int(self.length * 1000))

        create_H2_cable(     # with -01
            core_id=self.core.id,
            conduit_id=self.conduit.id,
            is_st_rod_E=False,
            with_01=True,
            length=int(self.length * 1000))

        cable = Product.objects.all().first()
        cable_2 = Product.objects.all()[1]

        self.assertEqual(cable.part_number, "100.М4(35)Г2.02500-01")
        self.assertEqual(len(cable.components), 15)
        self.assertEqual(cable_2.part_number, "100.М4(35)Г2.02500")
        self.assertEqual(len(cable_2.components), 15)

        core = cable.components.filter(item__title="Сердечник").first()
        conduit = cable.components.filter(item__title="Кожух").first()
        self.assertEqual(core.quantity, self.length - 0.135)
        self.assertEqual(conduit.quantity, self.length - 0.233)

    def test_H5_cable_creation(self):

        create_H5_cable(
            cable_type=0,
            core_id=self.core.id,
            conduit_id=self.conduit.id,
            is_st_rod_E=True,
            length=int(self.length * 1000))

        create_H5_cable(
            cable_type=2,
            core_id=self.core.id,
            conduit_id=self.conduit.id,
            is_st_rod_E=False,
            length=int(self.length * 1000))

        create_H5_cable(     # with -01
            cable_type=5,
            core_id=self.core.id,
            conduit_id=self.conduit.id,
            is_st_rod_E=False,
            length=int(self.length * 1000))

        cables = Product.objects.all()

        self.assertEqual(cables[2].part_number, "100.М4(40)22.02500")
        self.assertEqual(len(cables[2].components), 18)
        self.assertEqual(cables[1].part_number, "100.М4(40)Г5.02500")
        self.assertEqual(len(cables[1].components), 18)
        self.assertEqual(cables[0].part_number, "100.М4(40)22.02500-01")
        self.assertEqual(len(cables[0].components), 20)

        core = cables[2].components.filter(item__title="Сердечник").first()
        conduit = cables[2].components.filter(item__title="Кожух").first()
        self.assertEqual(core.quantity, self.length - 0.132)
        self.assertEqual(conduit.quantity, self.length - 0.275)

    def test_B_cable_creation(self):

        create_B_cable(
            cable_type=0,
            core_id=self.core.id,
            conduit_id=self.conduit.id,
            is_st_rods=False,
            is_st_sleeves=True,
            length=3008)

        create_B_cable(
            cable_type=1,
            core_id=self.core.id,
            conduit_id=self.conduit.id,
            is_st_rods=True,
            is_st_sleeves=False,
            length=3008)

        create_B_cable(
            cable_type=2,
            core_id=self.core.id,
            conduit_id=self.conduit.id,
            is_st_rods=True,
            is_st_sleeves=True,
            length=3024)

        create_B_cable(
            cable_type=3,
            core_id=self.core.id,
            conduit_id=self.conduit.id,
            is_st_rods=False,
            is_st_sleeves=False,
            length=3130)

        create_B_cable(
            cable_type=4,
            core_id=self.core.id,
            conduit_id=self.conduit.id,
            is_st_rods=False,
            is_st_sleeves=False,
            length=3160)

        cables = Product.objects.all()

        self.assertEqual(cables[4].part_number, "БП-М6323.03008")
        self.assertEqual(len(cables[4].components), 17)

        self.assertEqual(cables[3].part_number, "БП-М6323.03008-01")
        core = cables[3].components.filter(item__title="Сердечник").first()
        conduit = cables[3].components.filter(item__title="Кожух").first()
        self.assertEqual(core.quantity, 2.723)
        self.assertEqual(conduit.quantity, 2.523)
        self.assertEqual(len(cables[3].components), 17)

        self.assertEqual(cables[2].part_number, "БВ-М6323.03024")
        core = cables[2].components.filter(item__title="Сердечник").first()
        conduit = cables[2].components.filter(item__title="Кожух").first()
        self.assertEqual(core.quantity, 2.689)
        self.assertEqual(conduit.quantity, 2.493)
        self.assertEqual(len(cables[2].components), 16)

        self.assertEqual(cables[1].part_number, "БП-М6323.03130")
        core = cables[1].components.filter(item__title="Сердечник").first()
        conduit = cables[1].components.filter(item__title="Кожух").first()
        self.assertEqual(core.quantity, 2.815)
        self.assertEqual(conduit.quantity, 2.615)
        self.assertEqual(len(cables[1].components), 17)

        self.assertEqual(cables[0].part_number, "БВ-М6323.03160")
        core = cables[0].components.filter(item__title="Сердечник").first()
        conduit = cables[0].components.filter(item__title="Кожух").first()
        self.assertEqual(core.quantity, 2.815)
        self.assertEqual(conduit.quantity, 2.613)
        self.assertEqual(len(cables[0].components), 16)
