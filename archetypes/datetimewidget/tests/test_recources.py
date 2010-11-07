import unittest
from Products.CMFCore.utils import getToolByName

from archetypes.datetimewidget.tests.base import TestCase


class ResourceEnabledTest(TestCase):

    def test_portal_js(self):
        # this plugin is disabled by default. let's check if it's now enabled'
        js_id = "++resource++plone.app.jquerytools.dateinput.js"
        p_js = getToolByName(self.portal,'portal_javascripts')
        self.failUnless(p_js.getResource(js_id).getEnabled())
        
        
    def test_portal_css(self):
        # this stylesheet is disabled by default. let's check if it's now enabled
        css_id = "++resource++plone.app.jquerytools.dateinput.css"
        p_css = getToolByName(self.portal,'portal_css')
        self.failUnless(p_css.getResource(css_id).getEnabled())


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ResourceEnabledTest))
    return suite
