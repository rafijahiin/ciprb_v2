import os
import sys

os.environ['DATABASE_URL'] = 'sqlite:///db.sqlite3'

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ciprb.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line([sys.argv[0], "test", "baseline"])
