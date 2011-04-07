import unittest

from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite

# setup test content types
from Products.GenericSetup import EXTENSION, profile_registry

profile_registry.registerProfile('DatetimeWidget_examples',
    'DatetimeWidget Example Content Types',
    'Extension profile including Archetypes example content types',
    'profiles/examples',
    'archetypes.datetimewidget',
    EXTENSION)
ptc.setupPloneSite(extension_profiles=['archetypes.datetimewidget:default',])

import archetypes.datetimewidget

class TestCase(ptc.PloneTestCase):
    class layer(PloneSite):
        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            ztc.installPackage('archetypes.datetimewidget', quiet=0)
            zcml.load_config('configure.zcml',
                             archetypes.datetimewidget)
            fiveconfigure.debug_mode = False

        @classmethod
        def tearDown(cls):
            pass
