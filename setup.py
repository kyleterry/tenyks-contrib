#!/usr/bin/env python
from setuptools import setup, find_packages

version = '0.3.1'

setup(name='tenyks-contrib',
      version=version,
      description="Contributed services for the tenyks IRC bot",
      long_description="""\
""",
      classifiers=[],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='clients tenyks ircbot services tenyks-service',
      author='Kyle Terry',
      author_email='kyle@kyleterry.com',
      url='https://github.com/kyleterry/tenyks-contrib',
      license='LICENSE',
      packages=find_packages('src', exclude=['ez_setup', 'examples', 'tests']),
      package_dir={'': 'src'},
      package_data={'src': ['*.txt']},
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
          'tenyksservice>=2',
          'pyxDamerauLevenshtein'
          'feedparser',
          'python-dateutil',
          'requests',
          'nose',
          'pytz',
          'bs4'
      ],
      entry_points={
          'console_scripts': [
              'tenyksafk = tenyksafk.main:main',
              'tenyksfeeds = tenyksfeeds.main:main',
              'tenyksleetpoints = tenyksleetpoints.main:main',
              'tenyksmusic = tenyksmusic.main:main',
              'tenykssearch = tenykssearch.core:main',
              'tenykshahameter = tenykshahameter.main:main',
              'tenyksscripts = tenyksscripts.main:main',
              'tenykslinkscraper = tenykslinkscraper.main:main',
              'tenykslogger = tenykslogger.main:main',
              'tenykstwitter = tenykstwitter.main:main',
              'tenykswunderground = tenykswunderground.main:main',
              'tenykswebpagemonitor = webpage_monitor.main:main',
              'tenyksweblistener = tenyksweblistener.main:main',
              'tenyksddate = tenyksddate.main:main',
              'tenyksgentoo = tenyksgentoo.main:main',
              'tenykslol = tenykslol.main:main',
          ]
      },
      )
