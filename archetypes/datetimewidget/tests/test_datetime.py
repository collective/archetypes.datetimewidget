import unittest
from archetypes.datetimewidget.tests.base import TestCase
from Products.Archetypes.tests.utils import makeContent

class BaseWidgetTest(TestCase):
    
    fieldname = ''
    
    def afterSetUp(self):
        self.obj = makeContent(self.folder, portal_type='DatetimeWidgetType', id='datetime_test')
        self.field = self.obj.getField(self.fieldname)
        self.widget = self.field.widget
        

class DateWidgetTestCase(BaseWidgetTest):
    
    fieldname = 'datefield'
    
    def test_widget_properties(self):
        self.assertEqual(self.widget.macro, 'date_input')
        self.assertEqual(self.widget.value, self.widget.empty_value)
        self.assertEqual(self.widget.with_time, False)
        self.assertEqual(self.widget.show_day, True)
        
    def test_widget_process(self):
        self.assertFalse(self.widget.process_form(self.obj, self.field, {}))


class DatetimeWidgetTestCase(BaseWidgetTest):
    
    fieldname = 'datetimefield'
    
    def test_widget_properties(self):
        self.assertEqual(self.widget.macro, 'datetime_input')
        self.assertEqual(self.widget.value, self.widget.empty_value)
        self.assertEqual(self.widget.with_time, True)
        self.assertEqual(self.widget.ampm, 1)
        
    def test_widget_process(self):
        self.assertFalse(self.widget.process_form(self.obj, self.field, {}))


class MonthYearWidgetTestCase(BaseWidgetTest):
    
    fieldname = 'monthyearfield'
    
    def test_widget_properties(self):
        self.assertEqual(self.widget.macro, 'monthyear_input')
        self.assertEqual(self.widget.value, self.widget.empty_value)
        self.assertEqual(self.widget.show_day, False)
    
    def test_widget_process(self):
        self.assertFalse(self.widget.process_form(self.obj, self.field, {}))


def test_suite():
    from unittest import defaultTestLoader
    return defaultTestLoader.loadTestsFromName(__name__)
    
