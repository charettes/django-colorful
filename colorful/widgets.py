# -*- coding: utf-8 -*-
from django.forms.widgets import TextInput
from django.utils.safestring import SafeUnicode

class ColorFieldWidget(TextInput):
    class Media:
        css = {
            'all': ('css/colorful/colorPicker.css',)
        }
        js  = ('js/colorful/jquery.colorPicker.js',)
    
    input_type = 'color'
    
    def render_script(self, id):
        return u'''<script type="text/javascript">
                    (function($){
                        $(document).ready(function(){
                            $('#%s').each(function(i, elm){
                                # Make sure html5 color element is not replaced
                                if (elm.type != 'color') $(elm).colorPicker();
                            });
                        });
                    })(jQuery || django.jQuery);
                </script>
                ''' % id

    def render(self, name, value, attrs={}):
        if not 'id' in attrs:
            attrs['id'] = "#id_%s" % name
        render = super(ColorFieldWidget, self).render(name, value, attrs)
        return SafeUnicode(u"%s%s" % (render, self.render_script(attrs['id'])))