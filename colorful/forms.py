import re

from django.forms import RegexField

from .widgets import ColorFieldWidget

RGB_REGEX = re.compile(r'^#?((?:[0-F]{3}){1,2})$', re.IGNORECASE)


class RGBColorField(RegexField):
    """Form field for regular forms"""
    widget = ColorFieldWidget

    def __init__(self, **kwargs):
        kwargs['regex'] = RGB_REGEX
        super().__init__(**kwargs)
