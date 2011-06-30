from setuptools import setup, find_packages
import os

version = '0.9'

setup(name='archetypes.datetimewidget',
      version=version,
      description="A datetime widget for AT Content Types",
      long_description=open("README.txt").read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Simone Orsi',
      author_email='simahawk@gmail.com',
      url='https://github.com/collective/archetypes.datetimewidget',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['archetypes'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'Products.Archetypes',
          'Products.CMFCore',
          'Zope2',
          'plone.app.jquerytools',
          'zope.i18nmessageid',
      ],
      extras_require={
          'test': ['Products.DateRecurringIndex', # TODO: check this dep
                   'Products.GenericSetup',
                   'Products.PloneTestCase',
                   ]
          },
    )
