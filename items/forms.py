from django import forms

from django.contrib.auth.models import User

from .models import Item, Category, Product

from .helpers import get_choices


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
            self.add_error(
                'username',
                forms.ValidationError('Неправильний логін'),
            )
        else:
            if not user.check_password(password) and password:
                self.add_error(
                    'password',
                    forms.ValidationError('Неправильний пароль'),
                )
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


class AddOrderForm(forms.Form):

    customer = forms.CharField(label="Замовник")

    quantity = forms.FloatField(label="Кількість")

    product = forms.ChoiceField(label="Виріб", choices=[])

    # product field takes data from DB so it should
    # be updated each time when form requsted
    def __init__(self, *args, **kwargs):
        super(AddOrderForm, self).__init__(*args, **kwargs)
        products = Product.objects.order_by('-id')
        self.fields['product'].choices = [(product.id, "{} {} / {}".format(
            product.part_number,
            product.title,
            product.notes)) for product in products]


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

    serie = forms.ChoiceField(label="Серія", choices=SERIES)

    travel = forms.ChoiceField(label="Хід", choices=TRAVELS)

    mounting = forms.ChoiceField(label="Кріплення", choices=MOUNTINGS)

    length = forms.IntegerField(label="Довжина, мм")

    conduit = forms.ChoiceField(label="Кожух", choices=[])

    core = forms.ChoiceField(label="Сердечник", choices=[])

    is_st_rods = forms.BooleanField(label="Чорні прутки", required=False)

    is_st_sleeves = forms.BooleanField(label="Чорні трубки", required=False)

    is_plastic_sleeves = forms.BooleanField(label="Пластмасові трубки",
                                            required=False)

    def __init__(self, *args, **kwargs):
        super(AddStdCableForm, self).__init__(*args, **kwargs)

        conduits_category = Category.objects.filter(title="Кожух")
        conduits = Item.objects.filter(category=conduits_category)
        self.fields['conduit'].choices = get_choices(conduits)

        cores_category = Category.objects.filter(title="Сердечник")
        cores = Item.objects.filter(category=cores_category)
        self.fields['core'].choices = get_choices(cores)


class AddTZACableForm(forms.Form):

    conduit = forms.ChoiceField(label="Кожух", choices=[])

    core = forms.ChoiceField(label="Сердечник", choices=[])

    length = forms.IntegerField(label="Довжина, мм")

    is_st_rods = forms.BooleanField(label="Чорні прутки", required=False)

    def __init__(self, *args, **kwargs):
        super(AddTZACableForm, self).__init__(*args, **kwargs)

        conduits_category = Category.objects.filter(title="Кожух")
        conduits = Item.objects.filter(category=conduits_category)
        self.fields['conduit'].choices = get_choices(conduits)

        cores_category = Category.objects.filter(title="Сердечник")
        cores = Item.objects.filter(category=cores_category)
        self.fields['core'].choices = get_choices(cores)


class AddBCableForm(forms.Form):

    CABLES = (
        (0, "БП-М6323.03008"),
        (1, "БП-М6323.03008-01"),
        (2, "БВ-М6323.03024"),
        (3, "БП-М6323.03130"),
        (4, "БВ-М6323.03160"),)

    cable_type = forms.ChoiceField(label="Трос", choices=CABLES)

    length = forms.IntegerField(label="Довжина, мм", initial=3008)

    conduit = forms.ChoiceField(label="Кожух", choices=[])

    core = forms.ChoiceField(label="Сердечник", choices=[])

    is_st_rods = forms.BooleanField(label="Чорні прутки", required=False)

    is_st_sleeves = forms.BooleanField(label="Чорні трубки", required=False)

    def __init__(self, *args, **kwargs):
        super(AddBCableForm, self).__init__(*args, **kwargs)

        conduits_category = Category.objects.filter(title="Кожух")
        conduits = Item.objects.filter(category=conduits_category)
        self.fields['conduit'].choices = get_choices(conduits)

        cores_category = Category.objects.filter(title="Сердечник")
        cores = Item.objects.filter(category=cores_category)
        self.fields['core'].choices = get_choices(cores)


class DateRangeForm(forms.Form):

    range_start = forms.DateField(label="від")

    range_stop = forms.DateField(label="до")
