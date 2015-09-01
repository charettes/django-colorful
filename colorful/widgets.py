from __future__ import unicode_literals

import json

from django.forms.widgets import TextInput
from django.utils.safestring import mark_safe


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
