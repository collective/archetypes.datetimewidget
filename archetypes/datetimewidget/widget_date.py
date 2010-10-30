#-*- coding: utf-8 -*-

#############################################################################
#                                                                           #
#   Copyright (c) 2008 Rok Garbas <rok@garbas.si>                           #
#                                                                           #
# This program is free software; you can redistribute it and/or modify      #
# it under the terms of the GNU General Public License as published by      #
# the Free Software Foundation; either version 3 of the License, or         #
# (at your option) any later version.                                       #
#                                                                           #
# This program is distributed in the hope that it will be useful,           #
# but WITHOUT ANY WARRANTY; without even the implied warranty of            #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
# GNU General Public License for more details.                              #
#                                                                           #
# You should have received a copy of the GNU General Public License         #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.     #
#                                                                           #
#############################################################################


from datetime import date, datetime
from i18n import MessageFactory as _

from AccessControl import ClassSecurityInfo

from Products.Archetypes import Widget as widgets
from Products.Archetypes.Registry import registerWidget


class DateWidget(widgets.TypesWidget):
    """ Date widget. """
    
    _properties = widgets.TypesWidget._properties.copy()
    _properties.update({
        'macro' : 'date_input',
        'show_today_link' : False,
        'show_calendar' : True,
        'calendar_type' : 'gregorian',
        'klass' : u'date-widget',
        'value' : ('', '', ''),
        'show_jquerytools_dateinput' : False,
        'jquerytools_dateinput_config' : 'selectors: true, ' \
                                         'trigger: true, ' \
                                         'yearRange: [-10, 10]',
        'popup_calendar_icon' : '.css("background","url(popup_calendar.gif")' \
                          '.css("height", "16px")' \
                          '.css("width", "16px")' \
                          '.css("display", "inline-block")' \
                          '.css("vertical-align", "middle")',
    })
    
    def __call__(self, mode, instance, context=None):
        self.context = instance
        self.request = instance.REQUEST
        return super(DateWidget,self).__call__(mode, instance, context=context)
    
    @property
    def id(self):
        return self.getName()
    
    @property
    def name(self):
        return self.getName()
    
    security = ClassSecurityInfo()
    
    security.declarePublic('process_form')
    def process_form(self, instance, field, form, empty_marker=None,
                     emptyReturnsMarker=False, validating=True):
        """Basic impl for form processing in a widget"""
        
        fname = field.getName()
        value = form.get("%s-calendar" % fname, empty_marker)
        if value is empty_marker:
            return empty_marker
        # If JS support is unavailable, the value
        # in the request may be missing or incorrect
        # since it won't have been assembled from the
        # input components. Instead of relying on it,
        # assemble the date/time from its input components.
        year = form.get('%s-year' % fname, '0000')
        month = form.get('%s-month' % fname, '00')
        day = form.get('%s-day' % fname, '00')
        hour = form.get('%s-hour' % fname, '00')
        minute = form.get('%s-minute' % fname, '00')
        ampm = form.get('%s-ampm' % fname, '')
        if (year != '0000') and (day != '00') and (month != '00'):
            if ampm and ampm == 'PM' and hour != '12':
                hour = int(hour) + 12
            elif ampm and ampm == 'AM' and hour == '12':
                hour = '00'
            value = "%s-%s-%s %s:%s" % (year, month, day, hour, minute)
        else:
            value = ''
        if emptyReturnsMarker and value == '':
            return empty_marker
        # stick it back in request.form
#        form[fname] = value
        return value, {}
    
    
    @property
    def months(self):
        calendar = self.request.locale.dates.calendars[self.calendar_type]
        month_names = calendar.getMonthNames()
        for i, month in enumerate(month_names):
            yield dict(
                name     = month,
                value    = i+1,)

    @property
    def formatted_value(self):
        if self.value == ('', '', ''):
            return ''
        formatter = self.request.locale.dates.getFormatter("date", "short")
        date_value = date(*map(int, self.value))
        if date_value.year > 1900:
            return formatter.format(date_value)
        # due to fantastic datetime.strftime we need this hack
        # for now ctime is default
        return date_value.ctime()

    @property
    def year(self):
        year = self.request.get(self.name+'-year', None)
        if year:
            return year
        return self.value[0]

    @property
    def month(self):
        month = self.request.get(self.name+'-month', None)
        if month:
            return month
        return self.value[1]

    @property
    def day(self):
        day = self.request.get(self.name+'-day', None)
        if day:
            return day
        return self.value[2]

    def extract(self, default=None):
        # get normal input fields
        day = self.request.get(self.name + '-day', default)
        month = self.request.get(self.name + '-month', default)
        year = self.request.get(self.name + '-year', default)

        if not default in (year, month, day):
            return (year, month, day)

        # get a hidden value
        formatter = self.request.locale.dates.getFormatter("date", "short")
        hidden_date = self.request.get(self.name, '')
        try:
            dateobj = formatter.parse(hidden_date)
            return (str(dateobj.year),
                    str(dateobj.month),
                    str(dateobj.day))
        except zope.i18n.format.DateTimeParseError:
            pass

        return default

    def show_today_link_js(self):
        now = datetime.today()
        show_link_func = self.id+'-show-today-link'
        for i in ['-', '_']:
            show_link_func = show_link_func.replace(i, '')
        return '<a href="#" onclick="' \
            'document.getElementById(\'%(id)s-day\').value = %(day)s;' \
            'document.getElementById(\'%(id)s-month\').value = %(month)s;' \
            'document.getElementById(\'%(id)s-year\').value = %(year)s;' \
            'return false;">%(today)s</a>' % dict(
                id = self.id,
                day = now.day,
                month = now.month,
                year = now.year,
                today = zope.i18n.translate(_(u"Today"), context=self.request)
            )

    @property
    def language(self):
        return self.request.get('LANGUAGE', 'en')
    
    def show_jquerytools_dateinput_js(self, fieldName):
        calendar = self.request.locale.dates.calendars[self.calendar_type]
        localize =  'jq.tools.dateinput.localize("' + self.language + '", {'
        localize += 'months: "%s",' % ','.join(calendar.getMonthNames())
        localize += 'shortMonths: "%s",' % ','.join(calendar.getMonthAbbreviations())
        localize += 'days: "%s",' % ','.join(calendar.getDayNames())
        localize += 'shortDays: "%s",' % ','.join(calendar.getDayAbbreviations())
        localize += '});'
        return '''
            <input type="hidden" name="%(name)s-calendar"
                   class="%(name)s-calendar" />
            <script type="text/javascript">
                %(localize)s
                jq(".%(name)s-calendar").dateinput({%(config)s}).unbind('change')
                    .bind('onShow', function (event) {
                        var trigger_offset = jq(this).next().offset();
                        jq(this).data('dateinput').getCalendar().offset(
                            {top: trigger_offset.top+20, left: trigger_offset.left}
                        );
                    });
                jq(".%(name)s-calendar").next()%(popup_calendar_icon)s;

            </script>''' % dict(
                id=fieldName, name=fieldName,
                day=self.day, month=self.month, year=self.year,
                config=self.config_js, language=self.language, localize=localize,
                popup_calendar_icon=self.popup_calendar_icon,
            )
    
    @property
    def config_js(self):
        config = 'lang: "%s", ' % self.language
        if self.value != ('', '', ''):
            config += 'value: new Date(%s, %s, %s), ' % self.value
        config += 'change: function() { ' \
                    'var value = this.getValue("yyyy-mm-dd").split("-"); \n' \
                    'jq("#%(id)s-year").val(value[0]); \n' \
                    'jq("#%(id)s-month").val(value[1]); \n' \
                    'jq("#%(id)s-day").val(value[2]); \n' \
                '}, ' % dict(id = self.id)
        config += self.jquerytools_dateinput_config
        return config

            
registerWidget(DateWidget,
               title='Date widget',
               description=('Date widget'),
               used_for=('Products.Archetypes.Field.DateTimeField',)
               )
