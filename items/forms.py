from django import forms
from django.core.exceptions import ValidationError

from .models import Item


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
                    widget=forms.NumberInput,
                ),
            })

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