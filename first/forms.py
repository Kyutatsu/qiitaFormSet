from django import forms
from .models import TestModel



class TestForm(forms.Form):
    title = forms.CharField(max_length=20)
    date = forms.DateField()


class TestRadioForm(forms.ModelForm):
    class Meta:
        model = TestModel
        fields = ('text',)
        CHOICES = [
                ('first', 'FIRST'),
                ('second', 'SECOND'),
                ('third', 'THIRD'),
        ]
        widgets = {
                'text': forms.RadioSelect(choices=CHOICES),
        }


# prefix解説用
class FirstForm(forms.Form):
    name = forms.CharField(max_length=10)

class SecondForm(forms.Form):
    name = forms.CharField(max_length=10)
