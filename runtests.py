import os
import sys
from django.conf import settings

DIRNAME = os.path.dirname(__file__)

settings.configure(
    DEBUG=True,
    DATABASES={'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        }
    },
    TIME_ZONE='Europe/London',
    USE_TZ=True,
    INSTALLED_APPS=('django.contrib.auth',
                    'django.contrib.contenttypes',
                    'django.contrib.sessions',
                    'django.contrib.sites',
                    'django.contrib.messages',
                    'django.contrib.staticfiles',
                    'colorful',
                    ),
    )


# Cover both Django 1.6 and earlier
try:
    from django.test.runner import DiscoverRunner as TestRunner
except ImportError:
    from django.test.simple import DjangoTestSuiteRunner as TestRunner

test_runner = TestRunner(verbosity=1)
failures = test_runner.run_tests(['colorful', ])
if failures:
    sys.exit(failures)
