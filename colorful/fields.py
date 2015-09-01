from __future__ import unicode_literals

from django.core.validators import RegexValidator
from django.db.models import CharField

from . import forms, widgets


class RGBColorField(CharField):
    """Field for database models"""
    default_validators = [RegexValidator(regex=forms.RGB_REGEX)]

    def __init__(self, colors=None, *args, **kwargs):
        self.colors = colors
        kwargs['max_length'] = 7
        super(RGBColorField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs.update({
            'form_class': forms.RGBColorField,
            'widget': widgets.ColorFieldWidget(colors=self.colors),
        })
        return super(RGBColorField, self).formfield(**kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(RGBColorField, self).deconstruct()
        del kwargs['max_length']
        return name, path, args, kwargs
