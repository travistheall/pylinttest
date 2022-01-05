"""
Module to check requirements for used and unused packages.
"""
import os
import time
import pandas as pd


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
        base = base directory of the project
    """

    def __init__(self, base):
        self.base = base
        self.req = pd.DataFrame(columns=['pkg', 'used'])
        self.unused = pd.DataFrame(columns=['file_name', 'pkg'])
        self.errors = pd.DataFrame(columns=['pkg', 'used'])
        self.errors.set_index('pkg', inplace=True)
        self.unused.set_index('file_name', inplace=True)
        self.req.set_index('pkg', inplace=True)

    def make_reqs(self):
        """
        Reads the requirements.txt to create a list to check pylint results
        """
        with open(f'{self.base}\\requirements.txt', 'r') as file:
            requirements = [line.replace('\n', "") for line in file]
            for requirement in requirements:
                req_line = ''.join([character for character in requirement if character.isalpha()])
                req_line = req_line.strip()
                if req_line == 'os':
                    print('os')
                self.req = self.req.append(pd.DataFrame([0], index=[req_line], columns=['used']))

    def check_for_out_file(self):
        """
        lazy async await probably change the sleep to longer since bigger file
        """
        try:
            # fails if not there
            with open(f'{self.base}\\out.txt', 'r') as file:
                file.close()
        except FileNotFoundError:
            print('Line 57: FileNotFound sleep 5 seconds. Change me for longer wait')
            time.sleep(5)
            self.check_for_out_file()

    def run_pylint(self):
        """
        Creates an out.txt file that we will use to see if a particular package is used in a file
        """
        os.system(f'pylint --disable=all --enable=W0611 {self.base}\\proj > {self.base}\\out.txt')
        self.check_for_out_file()

    def set_unused(self):
        """
        sets global unused
        """
        not_used = []  # using a different name for func scope
        with open(f'{self.base}\\out.txt', 'r') as pylint_out:
            for line in pylint_out:
                # W0611 is unused-IMPORT error
                # text processing
                if line.find("W0611") != -1:
                    # line we care about is formatted like VVV
                    # proj\\mod\\unused1.py:6:0: W0611: Unused shape
                    # IMPORTed from numpy (unused-IMPORT)
                    line = line.replace('\n', "")
                    line = line.strip()
                    # file_in = proj\mod\unused1.py
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
        f_name = f_name.replace(f"{self.base}\\", "")
        with open(f_name, 'r') as file:
            for line in file:
                line = line.replace('\n', "")
                line = line.strip()
                line = line.split(" ")
                if line[0] in ["import", "from"]:
                    pkg = line[1].strip()
                    try:
                        unused_in_file = self.unused.loc[f_name]['pkg']
                        if isinstance(unused_in_file, str):
                            unused_in_file = pd.Series([unused_in_file])
                        else:
                            unused_in_file = unused_in_file.values
                        s_pkg = pd.Series([pkg])
                        if ~s_pkg.isin(unused_in_file).any() and s_pkg.isin(self.req.index).any():
                            self.req.at[pkg, 'used'] = 1
                        else:
                            self.append_to_errors(pkg)
                    except KeyError:
                        self.append_to_errors(pkg)

    def check_dir(self, dir_to_check):
        """
        Recursively look through directories
        :param dir_to_check: directory name
        """
        # ['proj', 'check.py', ...]
        for file_name in os.listdir(dir_to_check):
            dir_w_name = dir_to_check + "\\" + file_name
            if len(file_name.split(".")) == 1:  # if it's a directory
                # 'proj'.split(".") => ['proj'] => len == 1
                self.check_dir(dir_w_name)
            else:  # it's a file
                # 'check.py'.split(".") => ['Check', 'py'] => len == 2
                self.check_file(dir_w_name)

    def run(self):
        """
        Loop through all the directories
        """
        # ['proj', 'check.py', ...]
        base_dir = [x for x in os.listdir(self.base) if x not in ['.idea', '__pycache__', '.git']]
        for file in base_dir:
            if len(file.split(".")) == 1:  # if it's a directory
                # 'proj'.split(".") => ['proj'] => len == 1
                self.check_dir(f"{self.base}\\{file}")
            else:  # it's a file
                # 'check.py'.split(".") => ['Check', 'py'] => len == 2
                self.check_file(f"{self.base}\\{file}")

    def export_reqs(self):
        """
        Creates two files
        requirements.csv:
            contains all the packages from the requirements.txt and 0 if not used 1 if used
        not_in_requirements.csv:
            IMPORT statements that were not declared in requirements.txt but were used
        """
        self.req.index.rename('pkg', inplace=True)
        self.req.to_csv(f'{self.base}\\requirements.csv')
        self.errors.to_csv(f'{self.base}\\not_in_requirements.csv')
