import pandas as pd
import os
import time


class Check:
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
        self.req = []
        self.unused = []
        self.cols = ['pkg', 'used']
        self.ind = self.cols[0]
        self.fake_cols = [['foo', 0]]
        self.errors = pd.DataFrame(self.fake_cols, columns=self.cols)
        self.dirs = [item for item in os.listdir() if len(item.split(".")) == 1]
        self.errors.set_index('pkg', inplace=True)

    def make_reqs(self):
        """
        Reads the requirements.txt to create a list to check pylint results
        """
        with open(f'{self.base}\\requirements.txt', 'r') as file:
            requirements = [line.replace('\n', "") for line in file]
            for requirement in requirements:
                r = ''.join([character for character in requirement if character.isalpha()])
                r = r.strip()
                self.req.append(r)

    def check_for_out_file(self):
        try:
            f = open(f'{self.base}\\out.txt', 'r')
            f.close()
        except FileNotFoundError:
            # lazy async await probably change the sleep to longer since bigger file
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
        un = []  # un stands for unused im just lazy
        with open(f'{self.base}\\out.txt', 'r') as pylintout:
            for line in pylintout:
                # W0611 is unused-IMPORT error
                if line.find("W0611") != -1:
                    # text processing
                    # line we care about is formatted like VVV
                    # proj\mod\unused1.py:6:0: W0611: Unused shape IMPORTed from numpy (unused-IMPORT)
                    line = line.replace('\n', "")
                    line = line.strip()
                    # file_in = proj\mod\unused1.py
                    file_in = line.split(":")[0]
                    # ["Unused", "shape", "IMPORTed", "from", "numpy"]
                    line = line.split(":")[-1].split(" ")
                    for word in line:
                        word = word.strip()
                        if word in self.req:
                            # if the word is in the requirements.txt then its a module
                            # in this case numpy
                            un.append([file_in, word])

            un = pd.DataFrame(un, columns=['file_name', 'pkg'])
            un.set_index('file_name', inplace=True)
            self.unused = un

    def update_reqs(self):
        """
        Changes the list of requirements into a pandas data frame
        pkg: the package
        used: a boolean (well an int 0 or 1 where 0 means not used 1 means used)

        Init all are 0.
        Will Change to 1 when we find that it is used in the project
        """
        self.req = pd.DataFrame([[r, 0] for r in self.req], columns=self.cols)
        self.req.set_index(self.ind, inplace=True)

    def check_file(self, f_name):
        """
        Checks each individual file for the used and unused pacakges
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
                        if type(unused_in_file) == str:
                            unused_in_file = pd.Series(unused_in_file)
                        if not pd.Series([pkg]).isin(unused_in_file).any():
                            self.req.loc[pkg]['used'] = 1
                    except KeyError:
                        """
                        if it's not in the requirements.txt
                        nor already accounted for in errors df
                        account for it
                        """
                        if pkg not in self.req.index and pkg not in self.errors.index:
                            err = pd.DataFrame([{"pkg": pkg, 'used': 1}]).set_index("pkg")
                            self.errors = self.errors.append(err)

    def check_dir(self, dir_to_check):
        """
        Recursively look through directories
        :param dir_to_check: directory name
        """
        # ['proj', 'Check.py', ...]
        for n in os.listdir(dir_to_check):
            name = dir_to_check + "\\" + n
            if len(n.split(".")) == 1:  # if it's a directory
                # 'proj'.split(".") => ['proj'] => len == 1
                self.check_dir(name)
            else:  # it's a file
                # 'Check.py'.split(".") => ['Check', 'py'] => len == 2
                name = dir_to_check + "\\" + n
                self.check_file(name)

    def run(self):
        """
        Loop through all the directories
        """
        # ['proj', 'Check.py', ...]
        base_dir = [x for x in os.listdir(self.base) if x not in ['.idea', '__pycache__']]
        for file in base_dir:
            if len(file.split(".")) == 1:  # if it's a directory
                # 'proj'.split(".") => ['proj'] => len == 1
                self.check_dir(f"{self.base}\\{file}")
            else:  # it's a file
                # 'Check.py'.split(".") => ['Check', 'py'] => len == 2
                self.check_file(f"{self.base}\\{file}")

    def export_reqs(self):
        """
        Creates two files
        requirements.csv:
            contains all the packages from the requirements.txt and 0 if not used 1 if used
        not_in_requirements.csv:
            IMPORT statements that were not declared in requirements.txt but were used
        """
        self.req.to_csv(f'{self.base}\\requirements.csv')
        # [foo, 0] is the first row to get it to not yell at me
        # iloc[1:] to not have foo included
        self.errors.iloc[1:].to_csv(f'{self.base}\\not_in_requirements.csv')
