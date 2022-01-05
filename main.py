from Check import Check


if __name__ == '__main__':
    print('init')
    # base = "C:\\Users\\7J3234897\\PycharmProjects\\pylinttest"
    base = "Change Me"
    check = Check(base=base)
    check.make_reqs()
    print('linting')
    check.run_pylint()
    check.set_unused()
    check.update_reqs()
    print('running')
    check.run()
    check.export_reqs()
    print('done')
