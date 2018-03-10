from __future__ import unicode_literals

import json

from django.forms.widgets import CheckboxInput, MultiWidget, TextInput
from django.utils.safestring import mark_safe


class NullableColorFieldWidget(MultiWidget):
    def __init__(self, colors=None, attrs=None):
        _widgets = [
            CheckboxInput(attrs={'checked': 'checked', 'style': 'display:none'}),
            ColorFieldWidget(colors, attrs)
        ]
        super(NullableColorFieldWidget, self).__init__(_widgets, attrs)

    def decompress(self, value):
        if value:
            return [False, value]
        return [True, '']

    def value_from_datadict(self, data, files, name):
        blank = self.widgets[0].value_from_datadict(data, files, name + '_0')
        color = self.widgets[1].value_from_datadict(data, files, name + '_1')

        if blank:
            return None
        else:
            return color

    @staticmethod
    def render_script(color_id, checkbox_id):
        return '''
                <script type="text/javascript">
                    window.addEventListener('load', function() {
                        document.getElementById('%s').addEventListener('click', function() {
                            document.getElementById('%s').checked = false;
                        });
                    });
                </script>
                ''' % (color_id, checkbox_id)

    def render(self, name, value, attrs=None, renderer=None):
        parts = []
        checkbox_id = "id_%s_0" % name
        color_id = "id_%s_1" % name
        if value:
            self.widgets[0].attrs['checked'] = ''
        parts.append(super(NullableColorFieldWidget, self).render(name, value, attrs, renderer))
        parts.append(self.render_script(color_id, checkbox_id))
        return mark_safe(''.join(parts))


class ColorFieldWidget(TextInput):
    class Media:
        css = {
            'all': ("colorful/colorPicker.css",)
        }
        js = ("colorful/jQuery.colorPicker.js",)

    input_type = 'color'

    def __init__(self, colors=None, attrs=None):
        self.colors = colors
        super(ColorFieldWidget, self).__init__(attrs)

    def render_datalist(self, list_id):
        return ''.join([
            '<datalist id="%s">' % list_id,
            ''.join(['<option>%s</option>' % color for color in self.colors]),
            '</datalist>'
        ])

    def render_script(self, id):
        options = {}
        if self.colors:
            options['colors'] = [c.replace('#', '') for c in self.colors]
        return '''<script type="text/javascript">
                    (function($){
                        $(document).ready(function(){
                            $('#%s').each(function(i, elm){
                                // Make sure html5 color element is not replaced
                                if (elm.type != 'color') $(elm).colorPicker(%s);
                            });
                        });
                    })('django' in window && django.jQuery ? django.jQuery: jQuery);
                </script>
                ''' % (id, json.dumps(options))

    def render(self, name, value, attrs={}):
        parts = []
        if 'id' not in attrs:
            attrs['id'] = "id_%s" % name
        if self.colors:
            attrs['list'] = 'datalist_for_%s' % attrs['id']
            parts.append(self.render_datalist(attrs['list']))
        parts.append(super(ColorFieldWidget, self).render(name, value, attrs))
        parts.append(self.render_script(attrs['id']))
        return mark_safe(''.join(parts))
