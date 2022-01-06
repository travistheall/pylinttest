from check import CheckProj


if __name__ == '__main__':
    print('init')
    base = "C:\\Users\\7J3234897\\PycharmProjects\\pylinttest"
    # base = "Change Me"
    check = CheckProj(base=base)
    check.run()
    print('done')
