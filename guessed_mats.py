import parse_file
import numpy as np

def get_guessed_mats1(extra_prop):
    n = 4
    miss_matrix = np.zeros((n, n))
    hit_matrix = np.zeros((n, n))
    bright_matrix = np.zeros((n, n))
    
    miss_matrix[0, 1] = 0.5
    miss_matrix[1, 2] = 0.5
    miss_matrix[2, 3] = 0.5 - extra_prop

    bright_matrix[3, 1] = 1
    bright_matrix[2, 1] = extra_prop
    hit_matrix[2, 1] = 0.5
    hit_matrix[1, 0] = 0.5
    hit_matrix[0, 0] = 0.5

    return [miss_matrix, hit_matrix, bright_matrix]

def get_guessed_mats2(extra_prop):
    n = 4
    miss_matrix = np.zeros((n, n))
    hit_matrix = np.zeros((n, n))
    bright_matrix = np.zeros((n, n))
    
    miss_matrix[0, 1] = 0.5 - extra_prop
    miss_matrix[1, 2] = 0.5 - extra_prop
    miss_matrix[2, 3] = 0.5
    miss_matrix[1, 3] = extra_prop
    miss_matrix[0, 2] = extra_prop

    bright_matrix[3, 1] = 1
    hit_matrix[2, 1] = 0.5 
    hit_matrix[1, 0] = 0.5 
    hit_matrix[0, 0] = 0.5

    return [miss_matrix, hit_matrix, bright_matrix]

def get_guessed_mats3(extra_prop):
    n = 4
    miss_matrix = np.zeros((n, n))
    hit_matrix = np.zeros((n, n))
    bright_matrix = np.zeros((n, n))
    
    miss_matrix[0, 1] = 0.5 - 0
    miss_matrix[1, 2] = 0.5 - extra_prop
    miss_matrix[2, 3] = 0.5
    miss_matrix[1, 3] = extra_prop
    miss_matrix[0, 2] = 0

    bright_matrix[3, 1] = 1
    hit_matrix[2, 1] = 0.5 
    hit_matrix[1, 0] = 0.5 
    hit_matrix[0, 0] = 0.5

    return [miss_matrix, hit_matrix, bright_matrix]

def get_guessed_mats(extra_prop):
    return get_guessed_mats1(extra_prop)

def get_2way_mat(extra_prop):
    trans_mats_3way = get_guessed_mats(extra_prop)
    return [trans_mats_3way[0], trans_mats_3way[1] + trans_mats_3way[2]]