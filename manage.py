import os
import sys

import django
from django.conf import settings

import ceres_django_settings

if __name__ == "__main__":
    from dotenv import load_dotenv

    if os.path.exists(".env.dev"):
        load_dotenv(".env.dev")
    else:
        load_dotenv(".env")

    # CHANGED manage.py will use development settings by
    # default. Change the DJANGO_SETTINGS_MODULE environment variable
    # for using the environment specific settings file.
    settings.configure(default_settings=ceres_django_settings, DEBUG=True)
    django.setup()

    from django.core.management import execute_from_command_line

execute_from_command_line(sys.argv)