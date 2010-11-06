#-*- coding: utf-8 -*- 

__docformat__ = "reStructuredText"

from datetime import date, datetime
from z3c.form.converter import BaseDataConverter
from archetypes.datetimewidget.interfaces import DateValidationError, DatetimeValidationError

class DateDataConverter(BaseDataConverter):
    
    def toWidgetValue(self, value):
        if value is self.field.missing_value:
            return ('', '', '')
        return (value.year, value.month, value.day)

    def toFieldValue(self, value):
        for val in value:
            if not val:
                return self.field.missing_value

        try:
            value = map(int, value)
        except ValueError:
            raise DateValidationError
        try:
            return date(*value)
        except ValueError:
            raise DateValidationError

class DatetimeDataConverter(DateDataConverter):
    
    def toWidgetValue(self, value):
        if value is self.field.missing_value:
            return ('', '', '', '00', '00')
        return (value.year, value.month, value.day, value.hour, value.minute)

    def toFieldValue(self, value):
        for val in value:
            if not val:
                return self.field.missing_value

        try:
            value = map(int, value)
        except ValueError:
            raise DatetimeValidationError
        try:
            return datetime(*value)
        except ValueError:
            raise DatetimeValidationError

class MonthYearDataConverter(DateDataConverter):
    
    def toWidgetValue(self, value):
        if value is self.field.missing_value:
            return ('', '', '1')
        return (value.year, value.month, value.day)

