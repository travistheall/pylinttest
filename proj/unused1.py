"""
This is a file with a different import type
"""
import os
import time
import pandas as pd
from numpy import (
    shape,
    zeros
)
from scipy import rand

df = pd.DataFrame(rand)
print(os.getcwd())
