from setuptools import setup, find_packages
import sys, os

version = '0.1.0'

setup(name='tenyks-contrib',
      version=version,
      description="Contributed clients for the tenyks IRC bot",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='clients tenyks ircbot services tenyksclient',
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
      ],
      entry_points={
          'console_scripts': [
              'tenyksfeeds = tenyksfeeds.main:main',
              'tenyksmusic = tenyksmusic.main:main',
              'tenykssearch = tenykssearch.core:main',
          ]
      },
      )
