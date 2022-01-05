"""
This is a docstring to get pylint to be quiet.
"""
import os
import pandas as pd
from numpy import (
    shape,
    zeros
)
from scipy import rand

df = pd.DataFrame(rand)
print(os.getcwd())
