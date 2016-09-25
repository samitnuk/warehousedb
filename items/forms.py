from django import forms

from .models import Item, Category, Product


input_attrs = {'class': 'u-full-width'}


class AddProductForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)

        # quantity of additional fields depends of items quantity
        items = Item.objects.all()

        for item in items:
            self.fields.update({
                'item_%s' % item.id: forms.FloatField(
                    label='',
                    required=False,
                    widget=forms.NumberInput(
                        attrs={'class': 'table-input'}),), })

    title = forms.CharField(
        widget=forms.TextInput(attrs=input_attrs))
    part_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs=input_attrs))
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs=input_attrs))

    def fields_items(self):
        items = Item.objects.all()
        fields = []
        for item in items:
            fields.append([item, {'name': self['item_%s' % item.id]}])
        return fields


class AddOrderForm(forms.Form):

    customer = forms.CharField(
        label="Замовник",
        widget=forms.TextInput(attrs=input_attrs))

    quantity = forms.FloatField(
        label="Кількість",
        widget=forms.NumberInput(attrs=input_attrs))

    product = forms.ChoiceField(
        label="Виріб",
        choices=[],
        widget=forms.Select(attrs=input_attrs))

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
        (3, "#3 серія"),
        (4, "#4 серія"),
        (6, "#6 серія"),
        (8, "#8 серія"),)

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

    serie = forms.ChoiceField(
        label="Серія",
        choices=SERIES,
        widget=forms.Select(attrs=input_attrs))

    travel = forms.ChoiceField(
        label="Хід",
        choices=TRAVELS,
        widget=forms.Select(attrs=input_attrs))

    mounting = forms.ChoiceField(
        label="Кріплення",
        choices=MOUNTINGS,
        widget=forms.Select(attrs=input_attrs))

    length = forms.IntegerField(
        label="Довжина, мм",
        widget=forms.NumberInput(attrs=input_attrs))

    conduit = forms.ChoiceField(
        label="Кожух",
        choices=[],
        widget=forms.Select(attrs=input_attrs))

    core = forms.ChoiceField(
        label="Сердечник",
        choices=[],
        widget=forms.Select(attrs=input_attrs))

    # conduit and core fields take data from DB so they should
    # be updated each time when form requsted
    def __init__(self, *args, **kwargs):
        super(AddStdCableForm, self).__init__(*args, **kwargs)
        
        conduits_category = Category.objects.filter(name="Кожух")
        conduits = Item.objects.filter(category=conduits_category)
        self.fields['conduit'].choices = [(conduit.id, "{} {}".format(
            conduit.title,
            conduit.part_number)) for conduit in conduits]

        cores_category = Category.objects.filter(name="Сердечник")
        cores = Item.objects.filter(category=cores_category)
        self.fields['core'].choices = [(core.id, "{} {}".format(
            core.title,
            core.part_number)) for core in cores]

