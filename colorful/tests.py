from django.db import models
from unittest import TestCase
from django.core.exceptions import ValidationError

from .widgets import ColorFieldWidget
from .fields import RGBColorField


class TestModel(models.Model):
    color = RGBColorField()


class TestRBGColorField(TestCase):
    def setUp(self):
        self.field = RGBColorField()

    def test_validate_fails(self):
        """Test fails on:
        Empty, too short, invalid chars, too long
        """
        self.assertRaises(ValidationError, self.field.clean, '', None)
        self.assertRaises(ValidationError, self.field.clean, '12', None)
        self.assertRaises(ValidationError, self.field.clean, 'GGGGGG', None)
        self.assertRaises(ValidationError, self.field.clean, '#GGGGGG', None)
        self.assertRaises(ValidationError, self.field.clean, 'GGG', None)
        self.assertRaises(ValidationError, self.field.clean, '#GGG', None)
        self.assertRaises(ValidationError, self.field.clean, '#1234567', None)

        with self.assertRaises(ValidationError) as error:
            self.field.clean('#1234567', None)
            self.assertEqual(
                'Ensure this value has at most 7 characters (it has 8).',
                error.exception.message)

    def test_validate_passes(self):
        self.assertEqual('#123445', self.field.clean('#123445', None))
        self.assertEqual('#123', self.field.clean('#123', None))
        self.assertEqual('#ABCDEF', self.field.clean('#ABCDEF', None))
        self.assertEqual('ABCDEF', self.field.clean('ABCDEF', None))
        self.assertEqual('123', self.field.clean('123', None))
        self.assertEqual('ABC', self.field.clean('ABC', None))


class TestColorFieldWidget(TestCase):
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