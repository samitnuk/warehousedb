from django import forms

from .models import Item, Category


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
                    widget=forms.NumberInput,), })

    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'u-full-width'})
    )
    part_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'u-full-width'})
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'u-full-width'})
    )

    def fields_items(self):
        items = Item.objects.all()
        fields = []
        for item in items:
            fields.append([item, {'name': self['item_%s' % item.id]}])
        return fields

class AddStdCableForm(forms.Form):

    conduits_category = Category.objects.filter(name="Кожух")
    conduits = Item.objects.filter(category=conduits_category)
    CONDUITS = []
    for conduit in conduits:
        CONDUITS.append(
            [conduit.id, "%s - %s" % (conduit.title, conduit.part_number)])

    cores_category = Category.objects.filter(name="Сердечник")
    cores = Item.objects.filter(category=cores_category)
    CORES = []
    for core in cores:
        CORES.append(
            [core.id, "%s - %s" % (core.title, core.part_number)])

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
        (4, "5й хід (125 мм)"),)

    MOUNTINGS = (        
        ("22", "22 (різьба-різьба)"),
        ("23", "23 (різьба-клемп)"),
        ("33", "33 (клемп-клемп)"),)

    conduit = forms.ChoiceField(
        label="Кожух",
        choices=CONDUITS,
        widget=forms.Select(attrs={'class': 'u-full-width'}))
    core = forms.ChoiceField(
        label="Сердечник",
        choices=CORES,
        widget=forms.Select(attrs={'class': 'u-full-width'}))
    serie = forms.ChoiceField(
        label="Серія",
        choices=SERIES,
        widget=forms.Select(attrs={'class': 'u-full-width'}))
    travel = forms.ChoiceField(
        label="Хід",
        choices=TRAVELS,
        widget=forms.Select(attrs={'class': 'u-full-width'}))
    mounting = forms.ChoiceField(
        label="Кріплення",
        choices=MOUNTINGS,
        widget=forms.Select(attrs={'class': 'u-full-width'}))
    length = forms.FloatField(
        label="Довжина, мм",
        widget=forms.NumberInput(attrs={'class': 'u-full-width'}))