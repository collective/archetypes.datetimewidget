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

