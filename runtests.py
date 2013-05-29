#!/usr/bin/env python
import os, sys
from coverage import coverage
from optparse import OptionParser

from django.conf import settings

if not settings.configured:
    recurly_settings = {}
    try:
        from integration import *
    except ImportError:
        recurly_settings.update({
            'RECURLY_SUBDOMAIN': os.environ.get('RECURLY_SUBDOMAIN'),
            'RECURLY_API_KEY': os.environ.get('RECURLY_API_KEY'),
            'RECURLY_PRIVATE_KEY': os.environ.get('RECURLY_PRIVATE_KEY'),
            'RECURLY_DEFAULT_CURRENCY': 'USD',
            'USE_TZ': True
        })
    else:
        for key, value in locals().items():
            if key.startswith('RECURLY'):
                recurly_settings[key] = value

    from oscar import get_core_apps

    settings.configure(
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    }
                },
            INSTALLED_APPS=[
                'django.contrib.auth',
                'django.contrib.admin',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'django.contrib.sites',
                'oscar_recurly',
                ] + get_core_apps(),
            DEBUG=False,
            SITE_ID=1,
            NOSE_ARGS=['-s', '--with-spec'],
            **recurly_settings
        )

from django_nose import NoseTestSuiteRunner


def run_tests(*test_args):
    if 'south' in settings.INSTALLED_APPS:
        from south.management.commands import patch_for_test_db_setup
        patch_for_test_db_setup()

    if not test_args:
        test_args = ['oscar_recurly.tests']

    # Run tests
    test_runner = NoseTestSuiteRunner(verbosity=2)

    c = coverage(source=['oscar_recurly'], omit=['*migrations*', '*tests*'])
    c.start()
    num_failures = test_runner.run_tests(test_args)
    c.stop()

    if num_failures > 0:
        sys.exit(num_failures)
    print "Generating HTML coverage report"
    c.html_report()


def generate_migration():
    from south.management.commands.schemamigration import Command
    com = Command()
    com.handle(app='oscar_recurly', initial=True)


if __name__ == '__main__':
    parser = OptionParser()
    (options, args) = parser.parse_args()
    run_tests(*args)
