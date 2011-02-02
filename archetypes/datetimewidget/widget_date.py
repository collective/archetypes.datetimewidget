#-*- coding: utf-8 -*-

from datetime import date, datetime
from archetypes.datetimewidget.i18n import MessageFactory as _

from AccessControl import ClassSecurityInfo

from Products.Archetypes import Widget as widgets
from Products.Archetypes.Registry import registerWidget


class DateWidget(widgets.TypesWidget):
    """ Date widget. """

    empty_value = ('', '', '')
    calendar_icon_style = {'background':'url(popup_calendar.gif)',
                           'height':'16px',
                           'width':'16px',
                           'display':'inline-block',
                           'vertical-align':'middle'}

    _properties = widgets.TypesWidget._properties.copy()
    _properties.update({
        'macro' : 'date_input',
        'show_today_link' : False,
        'show_calendar' : True,
        'calendar_type' : 'gregorian',
        'klass' : u'date-widget',
        'show_day' : True,
        'with_time':False,
        'show_js_dateinput' : False,
        'js_dateinput_config' : 'selectors: true, ' \
                                'trigger: true, ' \
                                'yearRange: [-10, 10]',
        'popup_calendar_icon' : '.css(%s)' % str(calendar_icon_style),
    })

    def __call__(self, mode, instance, context=None):
        self.context = instance
        self.request = instance.REQUEST
        return super(DateWidget,self).__call__(mode, instance, context=context)
        
    def debugit(self, val):
        import pdb;pdb.set_trace()
        return val

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
        minute = form.get('%s-min' % fname, '00')
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
        form[fname] = value
        return value, {}
        
    def _padded_value(self, value):
        return str(value).zfill(2)
    
    @property
    def days(self):
        day_range = range(1,32)
        return [{'value':x,'label':self._padded_value(x)} for x in day_range]

    @property
    def months(self):
        calendar = self.request.locale.dates.calendars[self.calendar_type]
        month_names = calendar.getMonthNames()
        for i, month in enumerate(month_names):
            yield dict(name = month,
                       value = str(i+1), )
    
    @property
    def years(self):
        year_range = range(2000,2020)
        return [{'value':x,'label':x} for x in year_range]

    def get_formatted_value(self, value):
        if value == self.empty_value:
            return ''
        formatter = self.request.locale.dates.getFormatter("date", "short")
        datetime_value = datetime(*value.parts()[:6])
        if date_value.year > 1900:
            return formatter.format(date_value)
        # due to fantastic datetime.strftime we need this hack
        # for now ctime is default
        return date_value.ctime()

    @property
    def year(self):
        return self.value[0]

    @property
    def month(self):
        return self.value[1]

    @property
    def day(self):
        return self.value[2]

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

    def js_value(self, value):
        year = value.year
        month = value.month() - 1
        day = value.day()
        return 'new Date(%s, %s, %s), ' % (year, month, day)

    def config_js(self, value):
        config = 'lang: "%s", ' % self.language
        config += 'value: %s' % self.js_value(value)
        config += ('change: function() {\n'
                   '  var value = this.getValue();\n'
                   '  var parent = jQuery(this.getInput()).closest("div.%(parent_class)s");\n'
                   '  jQuery(parent).find(".year").val(value.getFullYear());\n'
                   '  jQuery(parent).find(".month").val(value.getMonth()+1);\n'
                   '  jQuery(parent).find(".day").val(value.getDate());\n'
                   '}, ') % dict(id = self.id,
                                 parent_class = self.name)
        config += self.js_dateinput_config
        return config

    @property
    def localize_js(self):
        calendar = self.request.locale.dates.calendars[self.calendar_type]
        localize =  'jQuery.tools.dateinput.localize("' + self.language + '", {'
        localize += 'months: "%s",' % ','.join(calendar.getMonthNames())
        localize += 'shortMonths: "%s",' % ','.join(calendar.getMonthAbbreviations())
        localize += 'days: "%s",' % ','.join(calendar.getDayNames())
        localize += 'shortDays: "%s",' % ','.join(calendar.getDayAbbreviations())
        localize += '});'
        return localize

    def get_js(self, fieldName, value):
        return '''
            <input type="hidden" id="%(name)s" name="%(name)s-calendar"
                   class="%(name)s-calendar" />
            <script type="text/javascript">
                %(localize)s
                jQuery(".%(name)s-calendar").dateinput({%(config)s}).unbind('change')
                    .bind('onShow', function (event) {
                        var trigger_offset = jQuery(this).next().offset();
                        jQuery(this).data('dateinput').getCalendar().offset(
                            {top: trigger_offset.top+20, left: trigger_offset.left}
                        );
                    });
                jQuery(".%(name)s-calendar").next()%(popup_calendar_icon)s;

            </script>''' % dict(
                id=fieldName, name=fieldName,
                day=self.day, month=self.month, year=self.year,
                config=self.config_js(value), language=self.language, localize=self.localize_js,
                popup_calendar_icon=self.popup_calendar_icon,
            )

registerWidget(DateWidget,
               title='Date widget',
               description=('Date widget'),
               used_for=('Products.Archetypes.Field.DateTimeField',)
               )
