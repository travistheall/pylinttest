"""
Module to check requirements for used and unused packages.
"""
import os
import time
import pandas as pd
from tqdm import tqdm


class CheckProj:
    """
    Class used to check if requirements are used in a project.
    Steps:
        1. Runs pylint to check files for unused packages
        2. Then checks IMPORT statements of files in modules
        3. Then updates whether a requirement was used
        4. Exports to a csv
            a. 0 = not used
            b. 1 = used
    Inputs:
        base = lint_dir directory of the project
    """

    def __init__(self, base):
        self.base = base
        self.proj = os.path.dirname(base)
        self.req = self.set_reqs()
        self.unused = pd.DataFrame(columns=['file_name', 'pkg'])
        self.errors = pd.DataFrame(columns=['pkg', 'used'])
        self.errors.set_index('pkg', inplace=True)
        self.unused.set_index('file_name', inplace=True)

    def set_reqs(self):
        """
        Reads the requirements.txt to create a list to check pylint results
        """
        req = pd.DataFrame(columns=['pkg', 'used'])
        req.set_index('pkg', inplace=True)

        symbs = ["==", ">", ">=", "<", "<=", "~=", "~", "@"]
        with open(os.path.join(self.proj, 'requirements.txt'), 'r') as file:
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

    def check_for_out_file(self):
        """
        lazy async await probably change the sleep to longer since bigger file
        """
        try:
            # fails if not there
            with open(os.path.join(self.base, 'out.txt'), 'r') as file:
                file.close()
        except FileNotFoundError:
            print('Line 57: FileNotFound sleep 5 seconds. Change me for longer wait')
            time.sleep(5)
            self.check_for_out_file()

    def set_unused(self):
        """
        sets global unused
        """
        not_used = []  # using a different name for func scope
        with open(os.path.join(self.base, 'out.txt'), 'r') as pylint_out:
            for line in pylint_out:
                # W0611 is unused-IMPORT error
                # text processing
                if line.find("W0611") != -1:
                    # line we care about is formatted like VVV
                    # proj\\proj_mod\\unused1.py:6:0: W0611: Unused shape
                    # IMPORTed from numpy (unused-IMPORT)
                    line = line.replace('\n', "")
                    line = line.strip()
                    # file_in = proj\proj_mod\unused1.py
                    file_in = line.split(":")[0]
                    # ["Unused", "shape", "IMPORTed", "from", "numpy"]
                    line = line.split(":")[-1].split(" ")
                    for word in line:
                        word = word.strip()
                        if word in self.req.index:
                            # if the word is in the requirements.txt then its a module
                            # in this case numpy
                            not_used.append([file_in, word])

            not_used = pd.DataFrame(not_used, columns=['file_name', 'pkg'])
            not_used.set_index('file_name', inplace=True)
            self.unused = not_used

    def run_pylint(self):
        """
        Creates an out.txt file that we will use to see if a particular package is used in a file
        """
        proj_out = os.path.join(self.base, 'out.txt')
        os.system(f'pylint --disable=all --enable=W0611 {self.proj} >> {proj_out}')
        self.check_for_out_file()
        self.set_unused()

    def append_to_errors(self, pkg):
        """
        if it's not in the requirements.txt
        nor already accounted for in errors df
        account for it
        """
        if pkg not in self.req.index and pkg not in self.errors.index:
            err = pd.DataFrame([{"pkg": pkg, 'used': 1}]).set_index("pkg")
            self.errors = self.errors.append(err)

    def check_file(self, f_name):
        """
        Checks each individual file for the used and unused packages
        Changes used from 0 to 1 if used.
        If it is used once then we should not remove it once iteration is over

        :param f_name: file name
        """
        with open(f_name, 'r') as file:
            proj = os.path.dirname(self.proj)+"/"
            f_name = f_name.replace(proj, '')
            for line in file:
                # looping through the lines to get the IMPORTed packages
                line = line.replace('\n', "")
                line = line.strip()
                line = line.split(" ")
                if line[0] in ["import", "from"]:
                    # txt process names of pkgs
                    pkg = line[1].strip()
                    try:
                        # see if the pkg was marked as unused in this file
                        # by pylint should return a series
                        unused_in_file = self.unused.loc[f_name]['pkg']
                        if isinstance(unused_in_file, str):
                            # if it returns a series convert to series
                            unused_in_file = pd.Series([unused_in_file])
                        else:
                            unused_in_file = unused_in_file.values
                        s_pkg = pd.Series([pkg])  # convert to series for series comp
                        # if not unused and is required then it's used
                        # if it's used once we don't want to remove it
                        if ~s_pkg.isin(unused_in_file).any() and s_pkg.isin(self.req.index).any():
                            # becomes requirements.csv
                            # if it's not changed to 1 in all iterations
                            # then it's not used
                            self.req.at[pkg, 'used'] = 1
                        else:
                            # otherwise the package is used in the file
                            # but it's not in the requirements
                            # os, time, etc
                            # becomes not_in_requirements.csv
                            self.append_to_errors(pkg)
                    except KeyError:
                        # if the package is used it'll will raise a key error
                        # errors in the prog but not errors irl
                        # becomes not_in_requirements.csv
                        self.append_to_errors(pkg)

    def loop_dir(self, directory):
        """
        Recursively look through directories
        :param directory: directory name
        """
        # ['proj', 'check.py', ...]
        for file_or_dir in tqdm(os.listdir(directory)):
            self.route_file_dir(directory, file_or_dir)

    def route_file_dir(self, parent_dir, file_or_dir):
        """
        :param file_or_dir: file name
        :param parent_dir: parent directory name
        """
        parent_w_child = os.path.join(parent_dir, file_or_dir)

        if len(file_or_dir.split(".")) == 1:  # if it's a directory
            # 'proj'.split(".") => ['proj'] => len == 1
            self.loop_dir(parent_w_child)
        elif file_or_dir.split(".")[1] == 'py':  # it's a py file
            # 'check.py'.split(".") => ['Check', 'py'] => len == 2
            self.check_file(parent_w_child)
        else:  # it's a reg  file
            pass

    def export_reqs(self):
        """
        Creates two files
        requirements.csv:
            contains all the packages from the requirements.txt and 0 if not used 1 if used
        not_in_requirements.csv:
            IMPORT statements that were not declared in requirements.txt but were used
        """
        self.req.to_csv(os.path.join(self.base, 'requirements.csv'))
        self.errors.to_csv(os.path.join(self.base, 'not_in_requirements.csv'))

    def run(self):
        """
        Main function to run prog
        Lints all files and
        Loops through all the directories
        """
        # ['proj', 'check.py', ...]
        print('linting')
        self.run_pylint()
        print('checking for unused requirements')
        proj_files = [x for x in os.listdir(self.proj) if x not in ['lint_dir']]
        for file_or_dir in tqdm(proj_files):
            self.route_file_dir(self.proj, file_or_dir)

        print('exporting')
        self.export_reqs()
        print('done')
