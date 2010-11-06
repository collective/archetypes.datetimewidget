#-*- coding: utf-8 -*- 

__docformat__ = "reStructuredText"

from widget_date import DateWidget

from AccessControl import ClassSecurityInfo

from Products.Archetypes import Widget as widgets
from Products.Archetypes.Registry import registerWidget


class MonthYearWidget(DateWidget):
    """ Month and year widget """
    
    empty_value = ('', '', 1)
    
    _properties = DateWidget._properties.copy()
    _properties.update({
        'macro' : 'monthyear_input',
        'klass' : u'monthyear-widget',
        'value' : empty_value,
        'show_day': False,
    })
    

registerWidget(MonthYearWidget,
               title='Month year widget',
               description=('Month year widget'),
               used_for=('Products.Archetypes.Field.DateTimeField',)
               )

