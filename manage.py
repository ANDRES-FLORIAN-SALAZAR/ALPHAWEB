"""Django's command-line utility for administrative tasks."""
import os
import sys

from django.core.management import execute_from_command_line

# Error messages
DJANGO_IMPORT_ERROR_MSG = (
    "Couldn't import Django. Are you sure it's installed and "
    "available on your PYTHONPATH environment variable? Did you "
    "forget to activate a virtual environment?"
)


def main() -> None:
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Alpha_web.settings")
    try:
        execute_from_command_line(sys.argv)
    except ImportError as exc:
        raise ImportError(DJANGO_IMPORT_ERROR_MSG) from exc


if __name__ == "__main__":
    main()
