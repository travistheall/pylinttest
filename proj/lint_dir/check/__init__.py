"""
Module to check requirements for used and unused packages.
"""
import os
import time
from datetime import datetime
import pandas as pd
from tqdm import tqdm
from .parse_requirements import parse_requirements
from .lint import Lint


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
        self.now = str(time.mktime(datetime.now().timetuple()))[:-2]
        self.base = base
        self.proj = os.path.dirname(base)
        self.out_file = os.path.join(base, f'out-{self.now}.txt')
        self.req = parse_requirements(self.proj)
        self.lint = Lint(base, self.now, self.req)
        self.unused = self.lint.unused
        self.not_in_req = pd.DataFrame(columns=['pkg', 'used'])
        self.not_in_req.set_index('pkg', inplace=True)

    def append_to_errors(self, pkg):
        """
        if it's not in the requirements.txt
        nor already accounted for in errors df
        account for it
        """
        if pkg not in self.req.index and pkg not in self.not_in_req.index:
            err = pd.DataFrame([{"pkg": pkg, 'used': 1}]).set_index("pkg")
            self.not_in_req = self.not_in_req.append(err)

    def parse_project_file(self, f_name):
        """
        Checks each individual file for the used and unused packages
        Changes used from 0 to 1 if used.
        If it is used once then we should not remove it once iteration is over

        :param f_name: file name
        """
        with open(f_name, 'r') as file:
            proj = os.path.dirname(self.proj)
            proj = os.path.join(proj, "")
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
        print(f'exporting to {not_req_csv}')
        self.not_in_req.to_csv(not_req_csv)

    def run(self):
        """
        Main function to run prog
        Lints all files and
        Loops through all the directories
        """
        # ['proj', 'check.py', ...]
        print('linting')
        self.lint.run()
        self.unused = self.lint.parse_out_file()
        print('checking for unused requirements')
        proj_files = [x for x in os.listdir(self.proj) if x not in ['lint_dir']]
        for file_or_dir in tqdm(proj_files):
            self.route_file_dir(self.proj, file_or_dir)

        self.export()
        print('done')
