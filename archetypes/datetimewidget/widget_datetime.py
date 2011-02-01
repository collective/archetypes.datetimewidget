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

    def js_value(self, value):
        year = value.year()
        month = value.month() - 1
        day = value.day()
        hour = value.hour()
        min = value.minute()
        return 'new Date(%s, %s, %s, %s, %s), ' % (
            year, month, day, hour, min)


registerWidget(DatetimeWidget,
               title='Datetime widget',
               description=('Datetime widget'),
               used_for=('Products.Archetypes.Field.DateTimeField',)
               )
