import calc_entropy
import parse_file

def get_guessed_mats(extra_prop):
    n = 4
    miss_matrix = np.zeros((n, n))
    hit_matrix = np.zeros((n, n))
    
    miss_matrix[0, 1] = 0.5
    miss_matrix[1, 2] = 0.5
    miss_matrix[2, 3] = 0.5 - extra_prop

    hit_matrix[3, 1] = 1
    hit_matrix[2, 1] = 0.5 + extra_prop
    hit_matrix[1, 0] = 0.5
    hit_matrix[0, 0] = 0.5

    return [miss_matrix, hit_matrix]