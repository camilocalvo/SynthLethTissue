import csv
import numpy as np
import pandas as pd
import pickle
import math

def checker(int_filename, sl_filename, cl_filename, types_filename):
    
    # Quartiles used for expression and essentiality
    q_ex = 25
    q_es = 25

    # Take interactions matrix (expression and essentiality data) 
    # Take SL Pairs
    # Take list of cell lines
    # Take list of tissue types

    data_sl = pd.read_csv(sl_filename, header=None)
    data_sl = data_sl.values.tolist()

    data_int = pickle.load( open(int_filename, "rb") )
    data_cl = pickle.load( open(cl_filename, "rb") )
    data_types = pickle.load( open(types_filename, "rb") )

    # Get values for expressivity and essentiality, corresponding percentiles
    # NOTE: -1 means higher essentiality, so bottom and top quartiles appear flipped

    expressivity = []
    essentiality = []
    for i in data_int:
        for j in data_int[i]:
            expressivity.append(data_int[i][j][1])
            essentiality.append(data_int[i][j][0])
    expressivity.sort()
    essentiality.sort()
    bottom_ex = np.percentile(expressivity, q_ex)
    top_ex = np.percentile(expressivity, 100-q_ex)
    top_es = np.percentile(essentiality, q_es)
    bottom_es = np.percentile(essentiality, 100-q_es)

    print([bottom_es,top_es])
    print(essentiality)

    # Create table of tissue type by SL (SL pairs are separated by ;)

    tissue_scores = {}
    for i in range(0, len(data_types)):
        SLs = {}
        for j in range(0, len(data_sl)):
            SL_str = data_sl[j][0] + ";" + data_sl[j][1]
            SLs[SL_str] = None
        tissue_scores[data_types[i]] = SLs
        
    # Go through each tissue type
    # Use the quartile cutoff to determine percent with the given SL

    for elem in data_int.keys():
        cur_type = data_cl[elem]
        for sl in data_sl:
            gene_1 = sl[0]
            gene_2 = sl[1]
            gene_str = gene_1 + ";" + gene_2
            es_1 = data_int[elem][gene_1][0]
            ex_1 = data_int[elem][gene_1][1]
            es_2 = data_int[elem][gene_2][0]
            ex_2 = data_int[elem][gene_2][1]

            # Check if this qualifies as SL
            # Less than for essentiality because more negative = more essential
            score = 0
            if ex_1 < bottom_ex and es_2 < top_es:
                score += .5
            if ex_2 < bottom_ex and es_1 < top_es:
                score += .5 
            
            if tissue_scores[cur_type][gene_str] == None:
                tissue_scores[cur_type][gene_str] = [1,score]
            else:
                num_cells = tissue_scores[cur_type][gene_str][0]
                old_score = tissue_scores[cur_type][gene_str][1]

                new_ratio = ((num_cells * old_score) + (score)) / (num_cells + 1)
                new_num_cells = num_cells + 1

                tissue_scores[cur_type][gene_str] = [new_num_cells,new_ratio]

    return tissue_scores