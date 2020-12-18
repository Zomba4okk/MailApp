from django import forms

from subscription.models import Request


class RequestCreateForm(forms.ModelForm):
    price = forms.IntegerField(label='Цена', initial=0, disabled=True)

    class Meta:
        model = Request
        fields = ('print_edition', 'duration')
        labels = {
            'print_edition': 'Издание',
            'duration': 'Длительность'
        }
