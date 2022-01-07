from check import CheckProj
import os

# cd /Users/yashbehal/projects/doorstep-django
# git clone https://github.com/travistheall/lint_dir

# PYCHARM SETTINGS CONFIG FILE SCRIPT PATH:
#       /Users/yashbehal/projects/doorstep-django/lint_dir/main.py
# PYCHARM SETTINGS CONFIG FILE PYTHON INTERPRETER:
#       python3 env with pandas
# IN A TERMINAL RUN:
#       pip3 install -r requirements.txt
#       from config working directory
# PYCHARM SETTINGS CONFIG FILE WORKING DIR:
#       /Users/yashbehal/projects/doorstep-django/lint_dir/

# PYCHARM SETTINGS CONFIG FILE OPTIONAL:
# OPEN EXCECUTION IN PYCHARM SETTINGS:
#       CHECK "Run with Python console."
#       This allows you to more easily debug.
#       see img.png for a picture of my config


# FILES OUTPUT DIR:
#   /Users/yashbehal/projects/doorstep-django/lint_dir/
# FILES:
#       not_in_requirements-timestamp.csv
#       requirements-timestamp.csv


if __name__ == '__main__':
    print('init')
    pylint_dir = os.getcwd()
    check = CheckProj(base=pylint_dir)
    check.run()
    print('program finished')
