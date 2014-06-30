from __future__ import unicode_literals

import re

from django.core.validators import RegexValidator
from django.db.models import CharField
from django.forms.fields import RegexField

from .widgets import ColorFieldWidget


RGB_REGEX = re.compile('^#?((?:[0-F]{3}){1,2})$', re.IGNORECASE)


class RGBColorField(CharField):
    widget = ColorFieldWidget
    default_validators = [RegexValidator(regex=RGB_REGEX)]

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 7
        super(RGBColorField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs.update({
            'form_class': RegexField,
            'widget': self.widget,
            'regex': RGB_REGEX
        })
        return super(RGBColorField, self).formfield(**kwargs)

    def south_field_triple(self):
        return 'colorful.fields.RGBColorField', [], {}

    def deconstruct(self):
        name, path, args, kwargs = super(RGBColorField, self).deconstruct()
        del kwargs['max_length']
        return name, path, args, kwargs
