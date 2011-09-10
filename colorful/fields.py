import re

from django.db.models import CharField
from django.forms.fields import RegexField

from widgets import ColorFieldWidget

RGB_REGEX = re.compile('^#?([0-F]{3}|[0-F]{6})$', re.IGNORECASE)

class RGBColorField(CharField):

    widget = ColorFieldWidget

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

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^colorful\.fields\.RGBColorField"])
except ImportError:
    pass
