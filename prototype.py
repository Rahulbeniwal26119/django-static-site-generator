import sys
import pathlib

from django.conf import settings


BASE_DIR = pathlib.Path(__file__).parent

settings.configure(
    DEBUG=True,
    SECRET_KEY='thisisthesecretkey',
    ROOT_URLCONF="sitebuilder.urls",
    MIDDLEWARE_CLASSES=(),
    INSTALLED_APPS=(
        'django.contrib.staticfiles',
        'sitebuilder',
        'compressor'
    ),
    STATIC_URL='/static/',
    TEMPLATES=(
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [BASE_DIR / 'templates'],
            'APP_DIRS': True,
        },
    ),
    SITE_PAGES_DIRECTORY=BASE_DIR / 'pages',
    SITE_OUTPUT_DIRECTORY=BASE_DIR / '_build',
    STATICFILES_DIRS=[
        BASE_DIR / 'static'
    ],
    STATIC_ROOT=BASE_DIR / '_build' / 'static',
    ALLOWED_HOSTS=['localhost', 'testserver'],
    STATICFILES_STORAGE='django.contrib.staticfiles.storage.ManifestStaticFilesStorage',
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'compressor.finders.CompressorFinder'
    )
)

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)