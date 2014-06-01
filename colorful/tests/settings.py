from __future__  import unicode_literals

from django.conf.global_settings import TEST_RUNNER


SECRET_KEY = 'not-anymore'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

INSTALLED_APPS = ['colorful']

if not TEST_RUNNER.endswith('DiscoverRunner'):
    TEST_RUNNER = 'discover_runner.DiscoverRunner'
