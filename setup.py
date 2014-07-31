#!/usr/bin/env python
from setuptools import setup, find_packages
import sys, os

version = '0.1.26'

setup(name='tenyks-contrib',
      version=version,
      description="Contributed clients for the tenyks IRC bot",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='clients tenyks ircbot services tenyks.client',
      author='Kyle Terry',
      author_email='kyle@kyleterry.com',
      url='https://github.com/kyleterry/tenyks-contrib',
      license='LICENSE',
      packages=find_packages('src', exclude=['ez_setup', 'examples', 'tests']),
      package_dir = {'':'src'},
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
          'tenyks',
          'tenyksservice==1.1',
          'feedparser',
          'python-dateutil',
          'flask',
          'requests'
      ],
      entry_points={
          'console_scripts': [
              'tenyksfeeds = tenyksfeeds.main:main',
              'tenyksleetpoints = tenyksleetpoints.main:main',
              'tenyksmusic = tenyksmusic.main:main',
              'tenykssearch = tenykssearch.core:main',
              'tenykshi = tenykshi.main:main',
              'tenyksfun = tenyksfun.main:main',
              'tenyksscripts = tenyksscripts.main:main',
              'tenykslinkscraper = tenykslinkscraper.main:main',
              'tenykslogger = tenykslogger.main:main',
              'tenykswunderground = tenykswunderground.main:main',
              'tenykswebpagemonitor = webpage_monitor.main:main',
              'tenyksweblistener = tenyksweblistener.main:main',
              'gentooservice = gentoo.main:main',
          ]
      },
      )
