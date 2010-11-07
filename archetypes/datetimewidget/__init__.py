#-*- coding: utf-8 -*-
__docformat__ = "reStructuredText"

from widget_date import DateWidget
from widget_datetime import DatetimeWidget
from widget_monthyear import MonthYearWidget

from Products.CMFCore.utils import ContentInit
from Products.Archetypes.atapi import process_types, listTypes
from Products.CMFCore.permissions import AddPortalContent

from archetypes.datetimewidget.config import PROJECTNAME


def initialize(context):
    """Initializer called when used as a Zope 2 product."""

    from archetypes.datetimewidget.examples import DatetimeWidgetType
    DatetimeWidgetType  # pyflakes
    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    ContentInit(
        PROJECTNAME + ' Content',
        content_types      = content_types,
        permission         = AddPortalContent,
        extra_constructors = constructors,
        ).initialize(context)
