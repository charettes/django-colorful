from __future__ import unicode_literals

import sys
# TODO: Remove when support for Python 2.6 is dropped
if sys.version_info >= (2, 7):
    from unittest import skipUnless
else:
    from django.utils.unittest import skipUnless

from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.test import SimpleTestCase

from ..fields import RGBColorField, RGB_REGEX
from ..widgets import ColorFieldWidget


class TestRBGColorField(SimpleTestCase):
    def setUp(self):
        self.field = RGBColorField()
        self.field_with_args = RGBColorField(default="#123445")

    def test_validate_fails(self):
        self.assertRaises(ValidationError, self.field.clean, '', None)
        self.assertRaises(ValidationError, self.field.clean, '12', None)
        self.assertRaises(ValidationError, self.field.clean, 'GGGGGG', None)
        self.assertRaises(ValidationError, self.field.clean, '#GGGGGG', None)
        self.assertRaises(ValidationError, self.field.clean, 'GGG', None)
        self.assertRaises(ValidationError, self.field.clean, '#GGG', None)
        self.assertRaises(ValidationError, self.field.clean, '#1234567', None)

        self.assertRaisesMessage(ValidationError, 'Ensure this value has at most 7 characters (it has 8).',
                                 self.field.clean, '#1234567', None)

    def test_validate_passes(self):
        self.assertEqual('#123445', self.field.clean('#123445', None))
        self.assertEqual('#123', self.field.clean('#123', None))
        self.assertEqual('#ABCDEF', self.field.clean('#ABCDEF', None))
        self.assertEqual('ABCDEF', self.field.clean('ABCDEF', None))
        self.assertEqual('123', self.field.clean('123', None))
        self.assertEqual('ABC', self.field.clean('ABC', None))

    def test_south_field_triple(self):
        path, args, kwargs = self.field.south_field_triple()
        module, cls = path.rsplit('.', 1)
        field_class = getattr(sys.modules[module], cls)
        field_instance = field_class(*args, **kwargs)
        self.assertIsInstance(field_instance, self.field.__class__)

    def test_south_field_triple_with_args(self):
        path, args, kwargs = self.field_with_args.south_field_triple()
        self.assertEqual(args, list())
        self.assertEqual(kwargs, {'default': "u'#123445'", 'max_length': '7'})

    @skipUnless(hasattr(models.Field, 'deconstruct'),
                'Unavailable field deconstruction.')
    def test_deconstruct(self):
        name, path, args, kwargs = self.field.deconstruct()
        self.assertIsNone(name)
        module, cls = path.rsplit('.', 1)
        field_class = getattr(sys.modules[module], cls)
        field_instance = field_class(*args, **kwargs)
        self.assertIsInstance(field_instance, self.field.__class__)

    def test_formfield(self):
        formfield = self.field.formfield()
        self.assertIsInstance(formfield, forms.RegexField)
        self.assertIsInstance(formfield.widget, ColorFieldWidget)
        self.assertEqual(formfield.regex, RGB_REGEX)


class TestColorFieldWidget(SimpleTestCase):
    def test_render_with_id(self):
        widget = ColorFieldWidget()
        self.assertIn('<input id="id_color" name="test" type="color" value="#123456" />',
                      widget.render('test', '#123456', {'id': 'id_color'}))
        self.assertIn('''<script type="text/javascript">
                    (function($){
                        $(document).ready(function(){
                            $('#id_color').each(function(i, elm){
                                // Make sure html5 color element is not replaced
                                if (elm.type != 'color') $(elm).colorPicker();
                            });
                        });
                    })('django' in window ? django.jQuery: jQuery);
                </script>
                ''', widget.render('test', '#123456', {'id': 'id_color'}))

    def test_render_no_id(self):
        widget = ColorFieldWidget()
        self.assertIn('<input id="id_test" name="test" type="color" value="#123456" />',
                      widget.render('test', '#123456'))
        self.assertIn('''<script type="text/javascript">
                    (function($){
                        $(document).ready(function(){
                            $('#id_test').each(function(i, elm){
                                // Make sure html5 color element is not replaced
                                if (elm.type != 'color') $(elm).colorPicker();
                            });
                        });
                    })('django' in window ? django.jQuery: jQuery);
                </script>
                ''', widget.render('test', '#123456'))
