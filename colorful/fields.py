from __future__ import unicode_literals

from django.core.validators import RegexValidator
from django.db.models import CharField

from . import forms
from .forms import RGB_REGEX
from .widgets import ColorFieldWidget


class RGBColorField(CharField):
    """Field for database models"""
    widget = ColorFieldWidget
    default_validators = [RegexValidator(regex=RGB_REGEX)]

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 7
        super(RGBColorField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs.update({
            'form_class': forms.RGBColorField,
            'widget': self.widget,
        })
        return super(RGBColorField, self).formfield(**kwargs)

    def south_field_triple(self):
        from south.modelsinspector import introspector
        args, kwargs = introspector(self)
        del kwargs['max_length']
        return 'colorful.fields.RGBColorField', args, kwargs

    def deconstruct(self):
        name, path, args, kwargs = super(RGBColorField, self).deconstruct()
        del kwargs['max_length']
        return name, path, args, kwargs
