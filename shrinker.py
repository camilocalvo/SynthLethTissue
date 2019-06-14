import csv
import numpy as np
import pandas as pd

def shrinker(csv1_filename, csv2_filename):

    shrink_cols = []
    for i in range(0,1000):
        shrink_cols.append(i)

    # Code to shrink the files so they're manageable
    data1 = pd.read_csv(csv1_filename, nrows=50, usecols=shrink_cols)
    data1.to_csv(path_or_buf="es.csv", index=False)

    data2 = pd.read_csv(csv2_filename, nrows=50, usecols=shrink_cols)
    data2.to_csv(path_or_buf="ex.csv", index=False)

    return 0