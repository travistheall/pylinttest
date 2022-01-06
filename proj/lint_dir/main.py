from check import CheckProj

# cd /Users/yashbehal/projects/doorstep_django
# git clone https://github.com/travistheall/pylinttest
# mv pylinttest/proj/lint_dir  ../..
# should end up /Users/yashbehal/projects/doorstep_django/lint_dir/main.py

if __name__ == '__main__':
    print('init')
    pylint_dir = "C:\\Users\\7J3234897\\PycharmProjects\\pylinttest\\proj\\lint_dir"
    # pylint_dir = "/Users/tnt/dev/pylinttest/proj/lint_dir"
    # pylint_dir = "/Users/yashbehal/projects/doorstep_django/lint_dir"
    # main.py and check.py should be here
    # out.txt, requirements.csv, and not_in_requirements.csv will be made here
    # I expect requirements.txt to be
    # /Users/yashbehal/projects/doorstep_django/requirement.txt
    check = CheckProj(base=pylint_dir)
    check.run()
    print('done')
