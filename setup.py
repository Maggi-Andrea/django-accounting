#!/usr/bin/env python
"""
Installation script:

To release a new version to PyPi:
- Ensure the version is correctly set in accounting.__init__.py
- Run:
    `python setup.py sdist`
    `twine upload dist/*`
"""
from setuptools import setup, find_packages
import os
import sys

from accounting import get_version

PROJECT_DIR = os.path.dirname(__file__)

setup(name='django-accounting',
      version=get_version().replace(' ', '-'),
      url='https://github.com/dulacp/django-accounting',
      author="Pierre Dulac",
      author_email="dulacpi@gmail.com",
      description="Accounting made accessible for small businesses and "
                  "sole proprietorships through a simple Django project",
      long_description=open(os.path.join(PROJECT_DIR, 'README.rst')).read(),
      keywords="Accounting, Django, Money, Cashflow",
      license='MIT',
      platforms=['linux'],
      packages=find_packages(exclude=["tests*"]),
      include_package_data=True,
      install_requires=[
          'django==2.1.7',
          # Used to render the forms
          'django-bootstrap4>=0.0.7',
          # Used to render the forms
          'django_icons>=0.2.1',
          # Used for date/time form fields
          'django-tempus-dominus>=5.1.2.2',
          # Used to improve the forms
          'django_select2==6.3.1',
          'django-crispy-forms>=1.7.2',
          # Define beautiful tags
          'django-classy-tags>=0.8.0',
          # Internationalization
          'Babel>=2.6.0',
          # Date utilities
          'python-dateutil>=2.8',
      ],
      # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Environment :: Web Environment',
          'Framework :: Django',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: Unix',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Topic :: Software Development :: Libraries :: Application Frameworks']
      )
