from django.utils.safestring import mark_safe
from django.forms import TextInput


class CalendarWidget(TextInput):
    class Media:
        css = {
            'all': ('/static/css/datepicker.css',)
        }
        js = ('/static/js/bootstrap-datepicker.js',
              '/static/js/datepicker_activation.js',
              )

    def render(self, name, value, attrs=None):
        return mark_safe(u'<div class=\"input-append date\" '
                         'id=\"dpYears\" data-date=\"2012-12-02\" '
                         'data-date-format=\"yyyy-mm-dd\" '
                         'data-date-viewmode=\"years\">'
                         '<input type=\"text\" '
                         'id=\"birth\"  name=\"birthday\" value=\"%s\">'
                         '<span class=\"add-on\"><i class="icon-calendar">'
                         '</i></span></div>' %
                         value
                         )
