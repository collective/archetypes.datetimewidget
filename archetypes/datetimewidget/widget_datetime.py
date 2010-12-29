#-*- coding: utf-8 -*-
__docformat__ = "reStructuredText"

from datetime import datetime
from archetypes.datetimewidget.widget_date import DateWidget

from Products.Archetypes.Registry import registerWidget


class DatetimeWidget(DateWidget):
    """ DateTime widget """

    empty_value = ('', '', '', '00', '00')

    _properties = DateWidget._properties.copy()
    _properties.update({
        'macro' : 'datetime_input',
        'value' : empty_value,
        'klass' : u'datetime-widget',
        'with_time': True,
        'ampm' : False,
    })

    def get_formatted_value(self, value):
        if value == self.empty_value:
            return ''
        formatter = self.request.locale.dates.getFormatter("dateTime", "short")
        datetime_value = datetime(*value.parts()[:6])
        if datetime_value.year > 1900:
            return formatter.format(datetime_value)
        # due to fantastic datetime.strftime we need this hack
        # for now ctime is default
        return datetime_value.ctime()

    @property
    def hour(self):
        return self.value[3]

    @property
    def minute(self):
        return self.value[4]

    def is_pm(self):
        if int(self.hour) >= 12:
            return True
        return False

    def padded_hour(self, hour):
        if self.ampm is True and self.is_pm() and int(hour)!=12:
            hour = str(int(hour)-12)
        return self._padded_value(hour)

    def padded_minute(self, minute):
        return self._padded_value(minute)
    
    @property
    def minutes(self):
        return [{'value':x,'label':self.padded_minute(x)} for x in range(60)]
        
    @property
    def hours(self):
        return [{'value':x,'label':self.padded_hour(x)} for x in range(24)]

    def extract(self, default=None):
        # get normal input fields
        day = self.request.get(self.name + '-day', default)
        month = self.request.get(self.name + '-month', default)
        year = self.request.get(self.name + '-year', default)
        hour = self.request.get(self.name + '-hour', default)
        minute = self.request.get(self.name + '-min', default)

        if (self.ampm is True and
            hour is not default and
            minute is not default and
            int(hour)!=12):
            ampm = self.request.get(self.name + '-ampm', default)
            if ampm == 'PM':
                hour = str(12+int(hour))
            # something strange happened since we either
            # should have 'PM' or 'AM', return default
            elif ampm != 'AM':
                return default

        if default not in (year, month, day, hour, minute):
            return (year, month, day, hour, minute)

        # get a hidden value
        formatter = self.request.locale.dates.getFormatter("dateTime", "short")
        hidden_date = self.request.get(self.name, '')
        try:
            dateobj = formatter.parse(hidden_date)
            return (str(dateobj.year),
                    str(dateobj.month),
                    str(dateobj.day),
                    str(dateobj.hour),
                    str(dateobj.minute))
        except zope.i18n.format.DateTimeParseError:
            pass

        return default

    @property
    def js_value(self):
        return 'new Date(%s, %s, %s, %s, %s), ' % self.value


registerWidget(DatetimeWidget,
               title='Datetime widget',
               description=('Datetime widget'),
               used_for=('Products.Archetypes.Field.DateTimeField',)
               )
