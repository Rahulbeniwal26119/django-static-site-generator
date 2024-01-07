import os
import shutil

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.shortcuts import resolve_url
from django.test.client import Client


def get_pages():
    for name in os.listdir(settings.SITE_PAGES_DIRECTORY):
        if name.endswith(".html"):
            yield name[:-5]

class Command(BaseCommand):
    help = "Build static site output."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('pages', nargs='*', help="Pages to build.")
    
    def handle(self, *args, **options):
        settings.DEBUG = False
        settings.COMPRESS_ENABLED = True

        pages = options['pages']
        if pages:
            available = list(get_pages())
            invalid = []

            for page in pages:
                if page not in available:
                    invalid.append(page)
            if invalid:
                msg = f"Invalid pages: {','.join(pages)}"
                raise CommandError(msg)
        else:
            pages = get_pages()

            if os.path.exists(settings.SITE_OUTPUT_DIRECTORY):
                shutil.rmtree(settings.SITE_OUTPUT_DIRECTORY)
            
            os.mkdir(settings.SITE_OUTPUT_DIRECTORY)
            os.makedirs(settings.STATIC_ROOT)

        call_command(command_name="collectstatic", interactive=False, clear=True, verbosity=0)
        call_command(command_name="compress", force=True)

        client = Client()

        for page in get_pages():
            url = resolve_url('page', slug=page)
            response = client.get(url)

            if page == 'index':
                output_dir = settings.SITE_OUTPUT_DIRECTORY
            else:
                output_dir = os.path.join(settings.SITE_OUTPUT_DIRECTORY, page)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
            
            with open(os.path.join(output_dir, 'index.html'), 'wb') as f:
                f.write(response.content)
