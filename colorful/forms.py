from __future__ import absolute_import, unicode_literals

import re

from django.forms import RegexField

from .widgets import ColorFieldWidget

RGB_REGEX = re.compile('^#?((?:[0-F]{3}){1,2})$', re.IGNORECASE)


class RGBColorField(RegexField):
    """Form field for regular forms"""
    widget = ColorFieldWidget

    def __init__(self, **kwargs):
        kwargs['regex'] = RGB_REGEX
        super(RGBColorField, self).__init__(**kwargs)
