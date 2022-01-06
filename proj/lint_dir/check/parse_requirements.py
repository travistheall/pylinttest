import pandas as pd
import os


def parse_requirements(proj):
    """
    Reads the requirements.txt to create a pandas dataframe to check pylint results
    """
    with open(os.path.join(proj, 'requirements.txt'), 'r') as file:
        reqs = pd.Series([line for line in file])
        reqs = reqs.str.replace('\n', "")

        def find_smb(r):
            symbs = ["==", ">", ">=", "<", "<=", "~=", "~", "@"]
            symb = [r.find(symb[0]) for symb in symbs if symb in r]
            if len(symb) > 0:
                return symb[0]
            else:
                return 0

        def find_name(r):
            if r['symbloc'] == 0:
                return r['pkg']
            else:
                return r['pkg'][:r['symbloc']]

        symb_loc = pd.DataFrame([reqs, reqs.apply(lambda r: find_smb(r))], index=['pkg', 'symbloc']).T
        pkg_names = symb_loc.apply(lambda r: find_name(r), axis='columns')
        pkg_names = pkg_names.rename('pkg')
        pkg_names = pkg_names.to_frame()
        pkg_names['used'] = 0
        pkg_names.set_index('pkg', inplace=True)
        return pkg_names
