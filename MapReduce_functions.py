from multiprocessing import Pool
from collections import defaultdict

def read_matrices(file_paths):
    matrices = []
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            matrices.append([list(map(float, row.split(','))) for row in file.readlines()])
    return matrices

def map_function(args):
    element, matrix_size = args
    matrix, i, j, value = element
    value = float(value)
    
    results = []

    if matrix == 'A':
        for k in range(matrix_size):
            results.append(((i, k), ('A', j, value)))
    elif matrix == 'B':
        for k in range(matrix_size):
            results.append(((k, j), ('B', i, value)))

    return results

def reduce_function(matrix_size, key_values_list):
    result = 0
    a_values = defaultdict(float)
    b_values = defaultdict(float)

    for key_values in key_values_list:
        key, (matrix, index, value) = key_values
        if matrix == 'A':
            a_values[index] += value
        elif matrix == 'B':
            b_values[index] += value

    for k in range(matrix_size):
        result += a_values[k] * b_values[k]

    return result

def mapreduce(matrices, matrix_size):
    elements = []

    for i in range(matrix_size):
        for j in range(matrix_size):
            elements.append(('A', i, j, matrices[0][i][j]))
            elements.append(('B', i, j, matrices[1][i][j]))

    with Pool() as pool:
        args = [(element, matrix_size) for element in elements]
        mapped_results = pool.map(map_function, args)

    reduced_result = reduce_function(matrix_size, [item for sublist in mapped_results for item in sublist])

    return reduced_result
