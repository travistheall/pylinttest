from check import CheckProj
import os

# cd /Users/yashbehal/projects/doorstep-django
# git clone https://github.com/travistheall/lint_dir
# should end up /Users/yashbehal/projects/doorstep-django/lint_dir/main.py

if __name__ == '__main__':
    print('init')
    pylint_dir = os.getcwd()
    # main.py and check.py should be here
    # out.txt, requirements.csv, and not_in_requirements.csv will be made here
    # I expect requirements.txt to be
    # /Users/yashbehal/projects/doorstep-django/requirement.txt
    check = CheckProj(base=pylint_dir)
    check.run()
    print('program finished')
