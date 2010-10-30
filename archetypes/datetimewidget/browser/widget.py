
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class DateWidget(BrowserView):
    """ """
    template = ViewPageTemplateFile('date_input.pt')

    @property
    def macros(self):
        return self.template.macros
    
    
class DatetimeWidget(BrowserView):
    """ """
    template = ViewPageTemplateFile('datetime_input.pt')

    @property
    def macros(self):
        return self.template.macros
    

class MonthYearWidget(BrowserView):
    """ """
    template = ViewPageTemplateFile('monthyear_input.pt')

    @property
    def macros(self):
        return self.template.macros


