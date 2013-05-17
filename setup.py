#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='django-oscar-recurly',
      version='0.0.1',
      url='https://github.com/mynameisgabe/django-oscar-recurly',
      author="Gabe Harriman",
      author_email="mynameisgabe@gmail.com",
      description="Recurly payment module for django-oscar",
      long_description=open('README.md').read(),
      keywords="Payment, Recurly",
      license='BSD',
      packages=find_packages(exclude=['sandbox*', 'tests*']),
      install_requires=['django-oscar>=0.3', 'requests>=0.13.5', 'recurly-client-python>=2.1.9'],
      dependency_links = [
        'https://github.com/recurly/recurly-client-python/tarball/master#egg=recurly-client-python-2.1.9',
      ],
      include_package_data=True,
      # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python']
      )
