from django.core.checks import Error
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db.models import CharField

from . import forms, widgets


class RGBColorField(CharField):
    """Field for database models"""
    widget = widgets.ColorFieldWidget
    default_validators = [RegexValidator(regex=forms.RGB_REGEX)]

    def __init__(self, *args, **kwargs):
        self.colors = kwargs.pop('colors', None)
        kwargs['max_length'] = 7
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs.update({
            'form_class': forms.RGBColorField,
            'widget': self.widget(colors=self.colors),
        })
        return super().formfield(**kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.colors is not None:
            kwargs['colors'] = self.colors
        del kwargs['max_length']
        return name, path, args, kwargs

    def check(self, **kwargs):
        errors = super().check(**kwargs)
        if self.colors is not None:
            if not isinstance(self.colors, (list, tuple)):
                errors.append(Error(
                    'colors is not iterable',
                    hint='Define the colors param as list of strings.',
                    obj=self,
                    id='colorful.E001'
                ))
            else:
                try:
                    for color in self.colors:
                        self.clean(color, None)
                except ValidationError:
                    errors.append(Error(
                        'colors item validation error',
                        hint='Each item of the colors param must be a valid '
                             'color string itself.',
                        obj=self,
                        id='colorful.E002'
                    ))
        return errors
