#-*- coding: utf-8 -*-

__docformat__ = "reStructuredText"

DOMAIN = 'archetypes.datetimewidget'
LANGUAGES= ['hr', 'sl', 'sr', 'sr_Latn', 'en', 'es', 'pt', 'de', 'fr', 'it']

import zope.i18nmessageid
MessageFactory = zope.i18nmessageid.MessageFactory(DOMAIN)

def sync():
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    os.system('i18ndude rebuild-pot --pot ' + \
                os.path.join(here,'locales', DOMAIN) + \
                '.pot --create ' + DOMAIN + ' ' + here)
    for lang in LANGUAGES:
        lang_path = os.path.join(here, 'locales', lang)
        if not os.path.isdir(lang_path):
            os.mkdir(lang_path)
        lang_path_lc = os.path.join(lang_path, 'LC_MESSAGES')
        if not os.path.isdir(lang_path_lc):
            os.mkdir(lang_path_lc)
        lang_file = os.path.join(lang_path_lc, DOMAIN)
        if not os.path.isfile(lang_file+'.po'):
            os.system('touch '+lang_file+'.po')
        os.system('i18ndude sync --pot ' + \
                    os.path.join(here,'locales', DOMAIN) + \
                    '.pot ' + lang_file + '.po')
        os.system('msgfmt -o ' + lang_file + '.mo ' + lang_file + '.po')





if __name__ == "__main__":
    sync()
