"""
Module to check requirements for used and unused packages.
"""
import os
import time
from datetime import datetime
import pandas as pd
from .parse_requirements import parse_requirements
# from .lint import Lint


class CheckProj:
    """
    Class used to check if requirements are used in a project.
    Steps:
        1. Then checks IMPORT statements of files in modules
        2. Then updates whether a requirement was used
        3. Exports to a csv (requirements.csv)
            a. 0 = not used
            b. 1 = used
        4. If an import is used but not in requirements.txt
            it is added to not_in_requirements.txt
            1 column.
            All packages in the file are used.
    Inputs:
        base = lint_dir directory of the project
    """

    def __init__(self, base):
        self.now = str(time.mktime(datetime.now().timetuple()))[:-2]
        self.base = base
        self.proj = os.path.dirname(base)
        self.out_file = os.path.join(base, f'out-{self.now}.txt')
        self.req = parse_requirements(self.proj)
        # self.lint = Lint(base, self.now, self.req)
        # self.unused = self.lint.unused
        self.not_in_req = pd.Series(name='pkg')

    def parse_project_file(self, f_name):
        """
        Checks each individual file for the used and unused packages
        Changes used from 0 to 1 if used.
        If it is used once then we should not remove it once iteration is over

        :param f_name: file name
        """
        with open(f_name, 'r') as file:
            lines = [line for line in file]
            lines = pd.Series(lines).str.strip()
            l_import = lines[lines.str.startswith('import')]
            f_import = lines[lines.str.startswith('from')]
            a_import = l_import.append(f_import)
            pkgs = a_import.str.split(" ", expand=True)[1].reset_index()[1]
            req_pkgs = pkgs[pkgs.isin(self.req.index)].reset_index()[1]
            self.req.at[req_pkgs, 'used'] = 1

            not_req_pkgs = pkgs[~pkgs.isin(self.req.index)].reset_index()[1]
            not_req_pkgs = not_req_pkgs.rename('pkg')
            self.not_in_req = self.not_in_req.append(not_req_pkgs, ignore_index=True)

    def loop_dir(self, directory):
        """
        Recursively look through directories
        :param directory: directory name
        """
        # ['proj', 'check.py', ...]
        for file_or_dir in os.listdir(directory):
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
            self.parse_project_file(parent_w_child)
        else:  # it's a reg  file
            pass

    def export(self):
        """
        Creates two files
        requirements-now.csv:
            contains all the packages from the requirements and 0 if not used 1 if used
        not_in_requirements-now.csv:
            IMPORT statements that were not declared in requirement.txt but were used
        """
        req_csv = os.path.join(self.base, f'requirements-{self.now}.csv')
        print(f'exporting to {req_csv}')
        self.req.to_csv(req_csv)
        not_req_csv = os.path.join(self.base, f'not_in_requirements-{self.now}.csv')
        self.not_in_req.drop_duplicates(keep='first', inplace=True)
        print(f'exporting to {not_req_csv}')
        self.not_in_req.to_csv(not_req_csv, index=False)

    def run(self):
        """
        Main function to run prog
        Loops through all the directories
        """
        # ['proj', 'check.py', ...]
        # print('linting')
        # self.lint.run()
        # self.unused = self.lint.parse_out_file()
        print('checking for unused requirements')
        proj_files = [x for x in os.listdir(self.proj) if x not in ['lint_dir']]
        for file_or_dir in proj_files:
            self.route_file_dir(self.proj, file_or_dir)

        self.export()
        print('check done')
