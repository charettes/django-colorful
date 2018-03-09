from __future__ import unicode_literals

import sys

from django import forms
from django.apps.registry import Apps
from django.core.checks import Error
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.fields import NOT_PROVIDED
from django.test import SimpleTestCase

from colorful.fields import RGBColorField
from colorful.forms import RGB_REGEX
from colorful.widgets import ColorFieldWidget, NullableColorFieldWidget

try:
    from unittest.mock import patch
except ImportError:  # py < 3.3
    from mock import patch


class TestRBGColorField(SimpleTestCase):
    def setUp(self):
        self.field = RGBColorField('verbose_name', default='#123445')
        self.field_with_colors = RGBColorField('verbose_name', colors=['#123445', '#000'])
        self.blank_field = RGBColorField('verbose_name', blank=True)

    def test_validate_fails(self):
        self.assertRaises(ValidationError, self.field.clean, '', None)
        self.assertRaises(ValidationError, self.field.clean, '12', None)
        self.assertRaises(ValidationError, self.field.clean, 'GGGGGG', None)
        self.assertRaises(ValidationError, self.field.clean, '#GGGGGG', None)
        self.assertRaises(ValidationError, self.field.clean, 'GGG', None)
        self.assertRaises(ValidationError, self.field.clean, '#GGG', None)
        self.assertRaises(ValidationError, self.field.clean, '#1234567', None)

        self.assertRaisesMessage(
            ValidationError,
            'Ensure this value has at most 7 characters (it has 8).',
            self.field.clean, '#1234567', None
        )

    def test_validate_passes(self):
        self.assertEqual('#123445', self.field.clean('#123445', None))
        self.assertEqual('#123', self.field.clean('#123', None))
        self.assertEqual('#ABCDEF', self.field.clean('#ABCDEF', None))
        self.assertEqual('ABCDEF', self.field.clean('ABCDEF', None))
        self.assertEqual('123', self.field.clean('123', None))
        self.assertEqual('ABC', self.field.clean('ABC', None))

    def test_deconstruct(self):
        name, path, args, kwargs = self.field.deconstruct()
        self.assertIsNone(name)
        module, cls = path.rsplit('.', 1)
        field_class = getattr(sys.modules[module], cls)
        field_instance = field_class(*args, **kwargs)
        self.assertIsInstance(field_instance, self.field.__class__)
        self.assertEqual(field_instance.verbose_name, self.field.verbose_name)
        self.assertEqual(field_instance.default, self.field.default)
        self.assertIsNone(field_instance.colors)

    def test_deconstruct_with_colors(self):
        name, path, args, kwargs = self.field_with_colors.deconstruct()
        self.assertIsNone(name)
        module, cls = path.rsplit('.', 1)
        field_class = getattr(sys.modules[module], cls)
        field_instance = field_class(*args, **kwargs)
        self.assertIsInstance(field_instance, self.field_with_colors.__class__)
        self.assertEqual(field_instance.verbose_name, self.field.verbose_name)
        self.assertEqual(field_instance.default, NOT_PROVIDED)
        self.assertEqual(field_instance.colors, field_instance.colors)

    def test_formfield(self):
        formfield = self.field.formfield()
        self.assertIsInstance(formfield, forms.RegexField)
        self.assertIsInstance(formfield.widget, ColorFieldWidget)
        self.assertEqual(formfield.regex, RGB_REGEX)

    @patch('django.db.models.CharField.check')
    def test_check(self, charfield_check):
        test_apps = Apps()

        # do not test django's charfield checks
        charfield_check.side_effect = list

        # fine fields from setUp
        self.assertEqual(self.field.check(), [])
        self.assertEqual(self.field_with_colors.check(), [])

        # check type error
        class ColorsTypeSystemCheckTestModel(models.Model):
            color = RGBColorField(colors='#333,#ff00FF')

            class Meta:
                apps = test_apps
                app_label = 'colorful'

        self.assertEqual(ColorsTypeSystemCheckTestModel.check(), [
            Error(
                'colors is not iterable',
                hint='Define the colors param as list of strings.',
                obj=ColorsTypeSystemCheckTestModel._meta.get_field('color'),
                id='colorful.E001'
            )
        ])

        # check item error
        class ColorsItemSystemCheckTestModel(models.Model):
            color = RGBColorField(colors=['#'])

            class Meta:
                apps = test_apps
                app_label = 'colorful'

        self.assertEqual(ColorsItemSystemCheckTestModel.check(), [
            Error(
                'colors item validation error',
                hint='Each item of the colors param must be a valid color '
                     'string itself.',
                obj=ColorsItemSystemCheckTestModel._meta.get_field('color'),
                id='colorful.E002'
            )
        ])

    def test_widget_selection(self):
        """
        When a RGBColorField has blank=True, the NullableColorFieldWidget should be used.
        When a RGBColorField has blank=False, the ColorFieldWidget should be used.
        """
        self.assertEqual(self.field.widget, ColorFieldWidget)
        self.assertEqual(self.blank_field.widget, NullableColorFieldWidget)


class TestColorFieldWidget(SimpleTestCase):
    def test_render_with_id(self):
        widget = ColorFieldWidget()
        self.assertInHTML(
            '<input id="id_color" name="test" type="color" value="#123456" />',
            widget.render('test', '#123456', {'id': 'id_color'})
        )
        self.assertIn('''<script type="text/javascript">
                    (function($){
                        $(document).ready(function(){
                            $('#id_color').each(function(i, elm){
                                // Make sure html5 color element is not replaced
                                if (elm.type != 'color') $(elm).colorPicker({});
                            });
                        });
                    })('django' in window && django.jQuery ? django.jQuery: jQuery);
                </script>
                ''', widget.render('test', '#123456', {'id': 'id_color'}))

    def test_render_no_id(self):
        widget = ColorFieldWidget()
        self.assertInHTML(
            '<input id="id_test" name="test" type="color" value="#123456" />',
            widget.render('test', '#123456')
        )
        self.assertIn('''<script type="text/javascript">
                    (function($){
                        $(document).ready(function(){
                            $('#id_test').each(function(i, elm){
                                // Make sure html5 color element is not replaced
                                if (elm.type != 'color') $(elm).colorPicker({});
                            });
                        });
                    })('django' in window && django.jQuery ? django.jQuery: jQuery);
                </script>
                ''', widget.render('test', '#123456'))

    def test_render_with_colors(self):
        widget = ColorFieldWidget(colors=['#ffffff', '#223344', '#557799'])
        self.assertInHTML(
            '<input id="id_test" list="datalist_for_id_test" name="test" type="color" value="#123456" />',
            widget.render('test', '#123456')
        )
        self.assertIn('''<script type="text/javascript">
                    (function($){
                        $(document).ready(function(){
                            $('#id_test').each(function(i, elm){
                                // Make sure html5 color element is not replaced
                                if (elm.type != 'color') $(elm).colorPicker({"colors": ["ffffff", "223344", "557799"]});
                            });
                        });
                    })('django' in window && django.jQuery ? django.jQuery: jQuery);
                </script>
                ''', widget.render('test', '#123456'))  # NOQA


class TestNullableColorFieldWidget(SimpleTestCase):

    def test_render_blank(self):
        widget = NullableColorFieldWidget()

        self.assertInHTML(
            '<input type="checkbox" name="test_0" checked="checked" style="display:none" />',
            widget.render('test', None)
        )
        self.assertInHTML(
            '<input name="test_1" type="color">',
            widget.render('test', None)
        )

    def test_render_with_value(self):
        widget = NullableColorFieldWidget()

        self.assertInHTML(
            '<input type="checkbox" name="test_0" style="display:none" checked />',
            widget.render('test', '#FFFFFF')
        )
        self.assertInHTML(
            '<input name="test_1" type="color" value="#FFFFFF">',
            widget.render('test', '#FFFFFF')
        )
