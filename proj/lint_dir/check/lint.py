"""
Do not use me.
I am going forward with the assumption that all imports are used
"""
import os
import time
import pandas as pd


class Lint:
    def __init__(self, base, now, req):
        self.now = now
        self.proj = os.path.dirname(base)
        self.req = req
        self.out_file = os.path.join(base, f'out-{self.now}.txt')
        self.unused = pd.DataFrame(columns=['file_name', 'pkg'])
        self.unused.set_index('file_name', inplace=True)

    def run(self):
        """
        Creates an out-now.txt file that we will use to see if a particular package is used in a file
        """
        os.system(f'pylint --disable=all --enable=W0611 {self.proj} > {self.out_file}')
        self.await_out_file()

    def await_out_file(self):
        """
        lazy async await probably change the sleep to longer since bigger file
        """
        try:
            # fails if not there
            with open(self.out_file, 'r') as file:
                file.close()
        except FileNotFoundError:
            print('Line 69: FileNotFound sleep 5 seconds. Change me for longer wait')
            time.sleep(5)
            self.await_out_file()

    def parse_out_file(self):
        """
        sets global unused
        """
        not_used = []  # using a different name for func scope
        with open(self.out_file, 'r') as pylint_out:
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
            return not_used
