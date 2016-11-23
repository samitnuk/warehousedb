from django.contrib.auth.models import User
from django.test import Client, TestCase

from .models import (Category, Item, ItemChange, Order, Component, Product,
                     Material, MaterialChange, Tool, ToolChange)

# from .utils import *
from . import utils


class UserTests(TestCase):

    def test_user_creation(self):

        user = User.objects.create(
            username='test_user',
            password='test_password')
        self.assertEqual(user.username, 'test_user')


class LoginTests(TestCase):

    def test_login(self):

        User.objects.create(username='test_user', password='test_password')
        c = Client()
        responce = c.post(
            '/login/',
            {'username': 'test_user', 'password': 'test_password'})
        self.assertEqual(responce.status_code, 200)


class ItemTests(TestCase):

    def test_category_creation(self):

        category = Category.objects.create(
            title="Тестова категорія",
            notes="Тестова нотатка")
        self.assertEqual(category.title, "Тестова категорія")
        self.assertEqual(category.notes, "Тестова нотатка")

    def test_item_creation(self):

        item = Item.objects.create(
            title="Деталь 1",
            part_number="00_123",
            part_number2="",
            picture="",
            category=Category.objects.create(
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

        itemchange = ItemChange.objects.first()

        self.assertEqual(itemchange.additional_quantity, -100)


class MaterialTests(TestCase):

    def test_material_creation(self):

        material = Material.objects.create(
            title="Матеріал",
            notes="Тестова нотатка матеріалу")
        self.assertEqual(material.title, "Матеріал")
        self.assertEqual(material.notes, "Тестова нотатка матеріалу")


class MaterialChangeTests(TestCase):

    fixtures = ['items/load_data.json']

    item = Item.objects.first()

    def test_materialchange_creation(self):

        material = Material.objects.create(
            title="Матеріал",
            notes="Тестова нотатка матеріалу")

        materialchange = MaterialChange.objects.create(
            additional_quantity=13,
            material=material,
            notes="Тестова нотатка")

        self.assertEqual(materialchange.material.title, "Матеріал")
        self.assertEqual(materialchange.material.notes,
                         "Тестова нотатка матеріалу")
        self.assertEqual(materialchange.additional_quantity, 13)
        self.assertEqual(materialchange.notes, "Тестова нотатка")

    def test_materialchange_auto_creation(self):

        material = Material.objects.create(
            title="Матеріал",
            notes="Тестова нотатка матеріалу")

        item_change = ItemChange.objects.create(
            additional_quantity=100,
            item=self.item,
            material=material,
            notes="Тестова нотатка")

        materialchange = MaterialChange.objects.first()
        add_qty = item_change.additional_quantity * self.item.rate * -1
        self.assertEqual(materialchange.additional_quantity, add_qty)


class ToolTests(TestCase):

    def test_tool_creation(self):

        tool = Tool.objects.create(
            title="Інструмент",
            notes="Тестова нотатка інструменту")
        self.assertEqual(tool.title, "Інструмент")
        self.assertEqual(tool.notes, "Тестова нотатка інструменту")


class ToolChangeTests(TestCase):

    def test_toolchange_creation(self):

        tool = Tool.objects.create(
            title="Інструмент",
            notes="Тестова нотатка інструменту")

        toolchange = ToolChange.objects.create(
            additional_quantity=13,
            tool=tool,
            notes="Тестова нотатка")

        self.assertEqual(toolchange.tool.title, "Інструмент")
        self.assertEqual(toolchange.tool.notes, "Тестова нотатка інструменту")
        self.assertEqual(toolchange.additional_quantity, 13)
        self.assertEqual(str(toolchange.tool), "Інструмент")
        self.assertEqual(toolchange.notes, "Тестова нотатка")


class ProductTests(TestCase):

    fixtures = ['items/load_data.json']

    conduit = Item.objects.filter(title="Кожух").first()
    core = Item.objects.filter(title="Сердечник").first()

    length = 2.500   # random number

    def test_std_cable_creation(self):

        utils.create_std_cable(
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

    def test_std_t_cable_creation(self):

        utils.create_std_t_cable(
            conduit_id=self.conduit.id,
            core_id=self.core.id,
            serie=4,
            travel=1,
            mounting="22",
            is_st_rods=True,
            length=int(self.length * 1000))

        utils.create_std_t_cable(
            conduit_id=self.conduit.id,
            core_id=self.core.id,
            serie=4,
            travel=3,
            mounting="23",
            is_st_rods=True,
            length=int(self.length * 1000))

        utils.create_std_t_cable(
            conduit_id=self.conduit.id,
            core_id=self.core.id,
            serie=4,
            travel=2,
            mounting="33",
            is_st_rods=False,
            length=int(self.length * 1000))

        cables = Product.objects.all()
        self.assertEqual(cables[0].part_number, "100.4M233.02500")
        self.assertEqual(len(cables[0].components), 6)
        self.assertEqual(cables[1].part_number, "100.4M323.02500")
        self.assertEqual(len(cables[1].components), 9)
        self.assertEqual(cables[2].part_number, "100.4M122.02500")
        self.assertEqual(len(cables[2].components), 8)

        core = cables[1].components.filter(item__title="Сердечник").first()
        conduit = cables[1].components.filter(item__title="Кожух").first()
        self.assertEqual(core.quantity, self.length - 0.057)
        self.assertEqual(conduit.quantity, self.length - 0.406)

    def test_tza_cable_creation(self):

        utils.create_tza_cable(
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

        utils.create_h4_cable(
            core_id=self.core.id,
            conduit_id=self.conduit.id,
            is_st_rod_e=False,
            length=int(self.length * 1000))

        cable = Product.objects.all().first()

        self.assertEqual(cable.part_number, "100.М4(40)Г4.02500")
        self.assertEqual(len(cable.components), 14)

        core = cable.components.filter(item__title="Сердечник").first()
        conduit = cable.components.filter(item__title="Кожух").first()
        self.assertEqual(core.quantity, self.length - 0.067)
        self.assertEqual(conduit.quantity, self.length - 0.174)

    def test_h2_cable_creation(self):

        utils.create_h2_cable(
            cable_type=6,
            core_id=self.core.id,
            conduit_id=self.conduit.id,
            is_st_rod_e=True,
            length=int(self.length * 1000))

        utils.create_h2_cable(     # with -01
            cable_type=7,
            core_id=self.core.id,
            conduit_id=self.conduit.id,
            is_st_rod_e=False,
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

    def test_h5_cable_creation(self):

        utils.create_h5_cable(
            cable_type=0,
            core_id=self.core.id,
            conduit_id=self.conduit.id,
            is_st_rod_e=True,
            length=int(self.length * 1000))

        utils.create_h5_cable(
            cable_type=2,
            core_id=self.core.id,
            conduit_id=self.conduit.id,
            is_st_rod_e=False,
            length=int(self.length * 1000))

        utils.create_h5_cable(     # with -01
            cable_type=5,
            core_id=self.core.id,
            conduit_id=self.conduit.id,
            is_st_rod_e=False,
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

    def test_b_cable_creation(self):

        utils.create_b_cable(
            cable_type=0,
            core_id=self.core.id,
            conduit_id=self.conduit.id,
            is_st_rods=False,
            is_st_sleeves=True,
            length=3008)

        utils.create_b_cable(
            cable_type=1,
            core_id=self.core.id,
            conduit_id=self.conduit.id,
            is_st_rods=True,
            is_st_sleeves=False,
            length=3008)

        utils.create_b_cable(
            cable_type=2,
            core_id=self.core.id,
            conduit_id=self.conduit.id,
            is_st_rods=True,
            is_st_sleeves=True,
            length=3024)

        utils.create_b_cable(
            cable_type=3,
            core_id=self.core.id,
            conduit_id=self.conduit.id,
            is_st_rods=False,
            is_st_sleeves=False,
            length=3130)

        utils.create_b_cable(
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
