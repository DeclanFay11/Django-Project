#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# https://www.youtube.com/watch?v=Yg5zkd9nm6w Watch this video 9/21
# https://www.youtube.com/watch?v=qDwdMDQ8oX4 or this guy
# https://www.youtube.com/watch?v=rDnWnQzTvGo

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storefront.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
