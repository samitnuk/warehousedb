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
        super(AddProductForm, self).__init__(*args, **kwargs)

        # quantity of additional fields depends of items quantity
        items = Item.objects.all()

        for item in items:
            self.fields.update({
                'item_{}'.format(item.id): forms.FloatField(
                    label='',
                    required=False), })

    title = forms.CharField(label="Найменування")

    part_number = forms.CharField(label="Індекс", required=False)

    notes = forms.CharField(label="Примітка", required=False,
                            widget=forms.Textarea)

    def get_form_data(self):
        items = Item.objects.all()
        categories = Category.objects.all()
        data = dict()
        for category in categories:
            if category not in data:
                data[category] = []
            items_q = items.filter(category=category)
            for item in items_q:
                data[category].append(
                    [item, {'name': self['item_{}'.format(item.id)]}])
        return data

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

    product_id = forms.ChoiceField(label="Виріб", choices=[])

    quantity = forms.FloatField(label="Кількість")

    notes = forms.CharField(label="Примітка", required=False,
                            widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(AddOrderForm, self).__init__(*args, **kwargs)
        products = Product.objects.order_by('-id')
        choices = [(product.id, "{} {} / {} | {}".format(
            product.part_number,
            product.title,
            product.notes,
            product.id)) for product in products]
        self.fields['product_id'].choices = choices

    def create_order(self):
        product_id = self.cleaned_data['product_id']
        Order.objects.create(
            customer=self.cleaned_data['customer'],
            product=Product.objects.filter(pk=product_id).first(),
            quantity=self.cleaned_data['quantity'],
            notes=self.cleaned_data['notes'])


class AddSentNotesToOrderForm(forms.Form):

    sent_notes = forms.CharField(label="Примітка", required=False,
                                 widget=forms.Textarea)

    def add_sent_notes(self):
        order = Order.objects.filter(pk=self.kwargs['pk'])
        order.update(
            is_sent=True,
            sent_notes=self.cleaned_data['sent_notes'])


class AbstractCableForm(forms.Form):
    """Base form for all cables"""

    conduit = forms.ChoiceField(label="Кожух", choices=[])

    core = forms.ChoiceField(label="Сердечник", choices=[])

    length = forms.IntegerField(label="Довжина, мм")

    def __init__(self, *args, **kwargs):
        super(AbstractCableForm, self).__init__(*args, **kwargs)

        conduits_category = Category.objects.filter(title="Кожух")
        conduits = Item.objects.filter(category=conduits_category)
        self.fields['conduit'].choices = get_choices(conduits)

        cores_category = Category.objects.filter(title="Сердечник")
        cores = Item.objects.filter(category=cores_category)
        self.fields['core'].choices = get_choices(cores)


class AddStdCableForm(AbstractCableForm):

    SERIES = ((4, "#4 серія"),
              (6, "#6 серія"),)

    serie = forms.ChoiceField(label="Серія", choices=SERIES)

    travel = forms.ChoiceField(label="Хід", choices=utils.TRAVELS)

    mounting = forms.ChoiceField(label="Кріплення", choices=utils.MOUNTINGS)

    is_st_rods = forms.BooleanField(label="Чорні прутки", required=False)

    is_st_sleeves = forms.BooleanField(label="Чорні трубки", required=False)

    is_plastic_sleeves = forms.BooleanField(label="Пластмасові трубки",
                                            required=False)

    field_order = [
            'conduit', 'core', 'serie', 'travel', 'mounting', 'is_st_rods',
            'is_st_sleeves', 'is_plastic_sleeves', 'length']

    def create_product(self):
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


class AddStdTCableForm(AbstractCableForm):

    SERIES = ((4, "#4 серія"),)

    serie = forms.ChoiceField(label="Серія", choices=SERIES)

    travel = forms.ChoiceField(label="Хід", choices=utils.TRAVELS)

    mounting = forms.ChoiceField(label="Кріплення", choices=utils.MOUNTINGS)

    is_st_rods = forms.BooleanField(label="Чорні прутки", required=False)

    field_order = ['conduit', 'core', 'serie', 'travel', 'mounting',
                   'is_st_rods', 'length']

    def create_product(self):
        utils.create_std_t_cable(
            conduit_id=self.cleaned_data['conduit'],
            core_id=self.cleaned_data['core'],
            serie=self.cleaned_data['serie'],
            travel=self.cleaned_data['travel'],
            mounting=self.cleaned_data['mounting'],
            is_st_rods=self.cleaned_data['is_st_rods'],
            length=self.cleaned_data['length'])


class AddTZACableForm(AbstractCableForm):

    is_st_rods = forms.BooleanField(label="Чорні прутки", required=False)

    field_order = ['conduit', 'core', 'is_st_rods', 'length']

    def create_product(self):
        utils.create_tza_cable(
            conduit_id=self.cleaned_data['conduit'],
            core_id=self.cleaned_data['core'],
            is_st_rods=self.cleaned_data['is_st_rods'],
            length=self.cleaned_data['length'])


class AddBCableForm(AbstractCableForm):

    cable_type = forms.ChoiceField(label="Трос", choices=utils.B_CABLES)

    is_st_rods = forms.BooleanField(label="Чорні прутки", required=False)

    is_st_sleeves = forms.BooleanField(label="Чорні трубки", required=False)

    length = forms.IntegerField(label="Довжина, мм", initial=3008)

    field_order = ['cable_type', 'conduit', 'core', 'is_st_rods',
                   'is_st_sleeves', 'length']

    def create_product(self):
        utils.create_b_cable(
            cable_type=self.cleaned_data['cable_type'],
            conduit_id=self.cleaned_data['conduit'],
            core_id=self.cleaned_data['core'],
            is_st_rods=self.cleaned_data['is_st_rods'],
            is_st_sleeves=self.cleaned_data['is_st_sleeves'],
            length=self.cleaned_data['length'])


class AddHCableForm(AbstractCableForm):

    cable_type = forms.ChoiceField(label="Трос", choices=utils.H_CABLES)

    is_st_rod_e = forms.BooleanField(label="Чорний пруток Е", required=False)

    length = forms.IntegerField(label="Довжина, мм", initial=1500)

    field_order = ['cable_type', 'conduit', 'core', 'is_st_rod_e', 'length']

    def create_product(self):
        utils.create_h_cable(
            cable_type=self.cleaned_data['cable_type'],
            conduit_id=self.cleaned_data['conduit'],
            core_id=self.cleaned_data['core'],
            is_st_rod_e=self.cleaned_data['is_st_rod_e'],
            length=self.cleaned_data['length'])


class DateRangeForm(forms.Form):

    range_start = forms.DateField(label="від")

    range_stop = forms.DateField(label="до")
