import csv
import numpy as np
import pandas as pd
import pickle

def cell_lines(cl_filename):
    
        # Find intersection of cell lines, intersection of genes
        # Build a matrix from the two

        data_cl = pd.read_csv(cl_filename)
        data_cl = data_cl.values.tolist()

        lines = {}
        for i in range(0,len(data_cl)):
                cur_type = data_cl[i][6]
                if cur_type != " ":
                        lines[data_cl[i][0]] = data_cl[i][6]

        pickle.dump(lines, open( "cell_lines.p", "wb" ))

        types = []
        for i in lines:
                cur_type = lines[i]
                if cur_type not in types:
                        types.append(cur_type)
        
        pickle.dump(types, open( "types.p", "wb" ))   

        return types

