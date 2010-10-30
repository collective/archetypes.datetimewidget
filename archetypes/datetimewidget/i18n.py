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


DOMAIN = 'archetypes.datetimewidget'
LANGUAGES= ['hr', 'sl', 'sr', 'sr_Latn', 'en', 'es', 'pt', 'de', 'fr', 'it']

try:
    import zope.i18nmessageid
    MessageFactory = zope.i18nmessageid.MessageFactory(DOMAIN)
except:
    pass


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
