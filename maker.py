import csv
import numpy as np
import pandas as pd
import pickle

def maker(es_filename, ex_filename):
    
    # Find intersection of cell lines, intersection of genes
    # Build a matrix from the two

    data_es = pd.read_csv(es_filename)
    data_ex = pd.read_csv(ex_filename)

    list_es = data_es.values.tolist()
    cell_lines_es = [i[0] for i in list_es]
    genes_es = data_es.columns.values.tolist()
    genes_es = genes_es[1:len(genes_es)]
    list_es = [i[1:len(list_es[0])] for i in list_es]

    list_ex = data_ex.values.tolist()
    cell_lines_ex = [i[0] for i in list_ex]
    genes_ex = data_ex.columns.values.tolist()
    genes_ex = genes_ex[1:len(genes_ex)]
    list_ex = [i[1:len(list_ex[0])] for i in list_ex]

    lines_intersect = intersection(cell_lines_es,cell_lines_ex)
    genes_intersect = intersection(genes_es,genes_ex)

    cell_indices = []
    for i in range(0,len(lines_intersect)):
        elem = lines_intersect[i]
        es_ind = cell_lines_es.index(elem)
        ex_ind = cell_lines_ex.index(elem)
        cell_indices.append([elem, es_ind, ex_ind])

    gene_indices = []
    for i in range(0,len(genes_intersect)):
        elem = genes_intersect[i]
        es_ind = genes_es.index(elem)
        ex_ind = genes_ex.index(elem)
        gene_indices.append([elem, es_ind, ex_ind])

    # Build up the dictionary of dictionaries

    compendium = {}
    for i in range(0,len(cell_indices)):
        es_row = cell_indices[i][1]
        ex_row = cell_indices[i][2]
        gene_row = {}
        for j in range(0,len(gene_indices)):
            pair = []
            es_col = gene_indices[j][1]
            ex_col = gene_indices[j][2]
            pair.append(list_es[es_row][es_col])
            pair.append(list_ex[ex_row][ex_col])
            gene_row[gene_indices[j][0]] = pair
        compendium[cell_indices[i][0]] = gene_row

    pickle.dump(compendium, open( "compendium.p", "wb" ))

    return compendium

def intersection(lst1, lst2): 
    return list(set(lst1) & set(lst2)) 