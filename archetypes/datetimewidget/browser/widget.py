
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class Base(BrowserView):

    @property
    def macros(self):
        return self.template.macros


class DateWidget(Base):
    """ view klass for DateWidget """
    template = ViewPageTemplateFile('datetime_input.pt')


class DatetimeWidget(Base):
    """ view klass for DatetimeWidget """
    template = ViewPageTemplateFile('datetime_input.pt')


class MonthYearWidget(Base):
    """ view klass for MonthYearWidget """
    template = ViewPageTemplateFile('datetime_input.pt')

