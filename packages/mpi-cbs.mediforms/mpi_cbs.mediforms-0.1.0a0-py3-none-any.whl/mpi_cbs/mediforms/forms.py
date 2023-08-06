from django import forms

from mpi_cbs.mediforms import models


class TokenForm(forms.ModelForm):
    class Meta:
        model = models.Token
        fields = 'method', 'pseudonym'
        help_texts = {
            'pseudonym': '(ID aus der Probandendatenbank)',
        }
