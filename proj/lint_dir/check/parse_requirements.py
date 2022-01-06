import pandas as pd
import os


def parse_requirements(proj):
    """
    Reads the requirements.txt to create a pandas dataframe to check pylint results
    """
    req = pd.DataFrame(columns=['pkg', 'used'])
    req.set_index('pkg', inplace=True)

    symbs = ["==", ">", ">=", "<", "<=", "~=", "~", "@"]
    with open(os.path.join(proj, 'requirements.txt'), 'r') as file:
        requirements = [line.replace('\n', "") for line in file]
        for requirement in requirements:
            # see what is separating versions
            symb = [symb for symb in symbs if symb in requirement]
            if len(symb) > 0:
                symb_loc = requirement.find(symb[0])
                req_line = requirement[:symb_loc].strip()
            else:
                req_line = requirement.strip()

            req = req.append(pd.DataFrame([0], index=[req_line], columns=['used']))

    req.index.rename('pkg', inplace=True)
    return req
