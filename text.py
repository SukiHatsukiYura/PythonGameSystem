
import random

def give_me_a_game(blank_size=9):
    matrix_all = build_game(matrix, 0, 0, random.choice(number_list))
    set_ij = set()
    while len(list(set_ij)) < blank_size:
        set_ij.add(str(random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8]))+','+str(random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8])))
    matrix_blank = [[col for col in row] for row in matrix_all]
    blank_ij = []
    for ij in list(set_ij):
        i, j = int(ij.split(',')[0]), int(ij.split(',')[1])
        blank_ij.append((i, j))
        matrix_blank[i][j] = 0
    return matrix_all, matrix_blank, blank_ij
