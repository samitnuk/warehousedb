from django import forms

from django.contrib.auth.models import User

from .models import Item, Category, Product, Order, Component

from .helpers import get_choices
from . import utils


class LoginForm(forms.Form):

    username = forms.CharField(label="Логін")

    password = forms.CharField(label="Пароль", widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.add_error('username',
                           forms.ValidationError('Неправильний логін'))
        else:
            if password and not user.check_password(password):
                self.add_error('password',
                               forms.ValidationError('Неправильний пароль'))
        return cleaned_data


class AddProductForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)

        # quantity of additional fields depends of items quantity
        items = Item.objects.all()

        for item in items:
            self.fields.update({
                'item_{}'.format(item.id): forms.FloatField(
                    label='',
                    required=False), })

    title = forms.CharField(label="Найменування")

    part_number = forms.CharField(label="Індекс", required=False)

    notes = forms.CharField(label="Примітка", required=False)

    def fields_items(self):
        items = Item.objects.all()
        fields = []
        for item in items:
            fields.append([item, {'name': self['item_{}'.format(item.id)]}])
        return fields

    def create_product(self):
        product = Product.objects.create(
            title=self.cleaned_data['title'],
            part_number=self.cleaned_data['part_number'],
            notes=self.cleaned_data['notes'])
        for item in Item.objects.all():
            quantity = self.cleaned_data['item_{}'.format(item.id)]
            if quantity is not None and float(quantity) > 0:
                Component.objects.create(product=product,
                                         item=item,
                                         quantity=quantity)


class AddOrderForm(forms.Form):

    customer = forms.CharField(label="Замовник")

    quantity = forms.FloatField(label="Кількість")

    product_id = forms.ChoiceField(label="Виріб", choices=[])

    def __init__(self, *args, **kwargs):
        super(AddOrderForm, self).__init__(*args, **kwargs)
        products = Product.objects.order_by('-id')
        self.fields['product_id'].choices = [(product.id, "{} {} / {}".format(
            product.part_number,
            product.title,
            product.notes)) for product in products]

    def create_order(self):
        product_id = self.cleaned_data['product_id']
        Order.objects.create(
            customer=self.cleaned_data['customer'],
            product=Product.objects.filter(pk=product_id).first(),
            quantity=self.cleaned_data['quantity'])


class AddStdCableForm(forms.Form):

    SERIES = (
        # (3, "#3 серія"),
        (4, "#4 серія"),
        (6, "#6 серія"),
        # (8, "#8 серія"),
    )

    TRAVELS = (
        (1, "1й хід (25 мм)"),
        (2, "2й хід (50 мм)"),
        (3, "3й хід (75 мм)"),
        (4, "4й хід (100 мм)"),
        (5, "5й хід (125 мм)"),)

    MOUNTINGS = (
        ("22", "22 (різьба-різьба)"),
        ("23", "23 (різьба-клемп)"),
        ("33", "33 (клемп-клемп)"),)

    conduit = forms.ChoiceField(label="Кожух", choices=[])

    core = forms.ChoiceField(label="Сердечник", choices=[])

    serie = forms.ChoiceField(label="Серія", choices=SERIES)

    travel = forms.ChoiceField(label="Хід", choices=TRAVELS)

    mounting = forms.ChoiceField(label="Кріплення", choices=MOUNTINGS)

    is_st_rods = forms.BooleanField(label="Чорні прутки", required=False)

    is_st_sleeves = forms.BooleanField(label="Чорні трубки", required=False)

    is_plastic_sleeves = forms.BooleanField(label="Пластмасові трубки",
                                            required=False)

    length = forms.IntegerField(label="Довжина, мм")

    def __init__(self, *args, **kwargs):
        super(AddStdCableForm, self).__init__(*args, **kwargs)

        conduits_category = Category.objects.filter(title="Кожух")
        conduits = Item.objects.filter(category=conduits_category)
        self.fields['conduit'].choices = get_choices(conduits)

        cores_category = Category.objects.filter(title="Сердечник")
        cores = Item.objects.filter(category=cores_category)
        self.fields['core'].choices = get_choices(cores)

    def create_std_cable(self):
        utils.create_std_cable(
            conduit_id=self.cleaned_data['conduit'],
            core_id=self.cleaned_data['core'],
            serie=self.cleaned_data['serie'],
            travel=self.cleaned_data['travel'],
            mounting=self.cleaned_data['mounting'],
            is_st_rods=self.cleaned_data['is_st_rods'],
            is_st_sleeves=self.cleaned_data['is_st_sleeves'],
            is_plastic_sleeves=self.cleaned_data['is_plastic_sleeves'],
            length=self.cleaned_data['length'])


class AddTZACableForm(forms.Form):

    conduit = forms.ChoiceField(label="Кожух", choices=[])

    core = forms.ChoiceField(label="Сердечник", choices=[])

    is_st_rods = forms.BooleanField(label="Чорні прутки", required=False)

    length = forms.IntegerField(label="Довжина, мм")

    def __init__(self, *args, **kwargs):
        super(AddTZACableForm, self).__init__(*args, **kwargs)

        conduits_category = Category.objects.filter(title="Кожух")
        conduits = Item.objects.filter(category=conduits_category)
        self.fields['conduit'].choices = get_choices(conduits)

        cores_category = Category.objects.filter(title="Сердечник")
        cores = Item.objects.filter(category=cores_category)
        self.fields['core'].choices = get_choices(cores)

    def create_tza_cable(self):
        utils.create_tza_cable(
            conduit_id=self.cleaned_data['conduit'],
            core_id=self.cleaned_data['core'],
            is_st_rods=self.cleaned_data['is_st_rods'],
            length=self.cleaned_data['length'])


class AddBCableForm(forms.Form):

    cable_type = forms.ChoiceField(label="Трос", choices=utils.B_CABLES)

    conduit = forms.ChoiceField(label="Кожух", choices=[])

    core = forms.ChoiceField(label="Сердечник", choices=[])

    is_st_rods = forms.BooleanField(label="Чорні прутки", required=False)

    is_st_sleeves = forms.BooleanField(label="Чорні трубки", required=False)

    length = forms.IntegerField(label="Довжина, мм", initial=3008)

    def __init__(self, *args, **kwargs):
        super(AddBCableForm, self).__init__(*args, **kwargs)

        conduits_category = Category.objects.filter(title="Кожух")
        conduits = Item.objects.filter(category=conduits_category)
        self.fields['conduit'].choices = get_choices(conduits)

        cores_category = Category.objects.filter(title="Сердечник")
        cores = Item.objects.filter(category=cores_category)
        self.fields['core'].choices = get_choices(cores)

    def create_b_cable(self):
        utils.create_b_cable(
            cable_type=self.cleaned_data['cable_type'],
            conduit_id=self.cleaned_data['conduit'],
            core_id=self.cleaned_data['core'],
            is_st_rods=self.cleaned_data['is_st_rods'],
            is_st_sleeves=self.cleaned_data['is_st_sleeves'],
            length=self.cleaned_data['length'])


class AddHCableForm(forms.Form):

    cable_type = forms.ChoiceField(label="Трос", choices=utils.H_CABLES)

    conduit = forms.ChoiceField(label="Кожух", choices=[])

    core = forms.ChoiceField(label="Сердечник", choices=[])

    is_st_rod_e = forms.BooleanField(label="Чорний пруток Е", required=False)

    length = forms.IntegerField(label="Довжина, мм", initial=1500)

    def __init__(self, *args, **kwargs):
        super(AddHCableForm, self).__init__(*args, **kwargs)

        conduits_category = Category.objects.filter(title="Кожух")
        conduits = Item.objects.filter(category=conduits_category)
        self.fields['conduit'].choices = get_choices(conduits)

        cores_category = Category.objects.filter(title="Сердечник")
        cores = Item.objects.filter(category=cores_category)
        self.fields['core'].choices = get_choices(cores)

    def create_h_cable(self):
        utils.create_h_cable(
            cable_type=self.cleaned_data['cable_type'],
            conduit_id=self.cleaned_data['conduit'],
            core_id=self.cleaned_data['core'],
            is_st_rod_e=self.cleaned_data['is_st_rod_e'],
            length=self.cleaned_data['length'])


class DateRangeForm(forms.Form):

    range_start = forms.DateField(label="від")

    range_stop = forms.DateField(label="до")
