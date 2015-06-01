from __future__ import unicode_literals

from django.forms.widgets import TextInput
from django.utils.safestring import mark_safe


class ColorFieldWidget(TextInput):
    class Media:
        css = {
            'all': ("colorful/colorPicker.css",)
        }
        js = ("colorful/jQuery.colorPicker.js",)

    input_type = 'color'

    def render_script(self, id):
        return '''<script type="text/javascript">
                    (function($){
                        $(document).ready(function(){
                            $('#%s').each(function(i, elm){
                                // Make sure html5 color element is not replaced
                                if (elm.type != 'color') $(elm).colorPicker();
                            });
                        });
                    })('django' in window && django.jQuery ? django.jQuery: jQuery);
                </script>
                ''' % id

    def render(self, name, value, attrs={}):
        if 'id' not in attrs:
            attrs['id'] = "id_%s" % name
        render = super(ColorFieldWidget, self).render(name, value, attrs)
        return mark_safe("%s%s" % (render, self.render_script(attrs['id'])))
