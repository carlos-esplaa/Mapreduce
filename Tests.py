from multiprocessing import Pool
import time
import numpy as np
import csv
import os
import matplotlib.pyplot as plt
from MapReduce_functions import mapreduce, read_matrices

def generate_random_matrix(rows, cols):
    return np.random.rand(rows, cols)

def save_matrix_to_csv(matrix, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in matrix:
            writer.writerow(row)

def run_matrix_multiplication(matrix_size):
    matrix_a = generate_random_matrix(matrix_size, matrix_size)
    matrix_b = generate_random_matrix(matrix_size, matrix_size)

    filename_a = os.path.join(csv_directory, f'matrix_a_{matrix_size}x{matrix_size}.csv')
    filename_b = os.path.join(csv_directory, f'matrix_b_{matrix_size}x{matrix_size}.csv')

    save_matrix_to_csv(matrix_a, filename_a)
    save_matrix_to_csv(matrix_b, filename_b)

    matrices = read_matrices([filename_a, filename_b])

    start_time = time.time()

    result = mapreduce(matrices, matrix_size)

    end_time = time.time()
    elapsed_time = round(end_time - start_time, 2)  # Redondear a dos decimales

    return elapsed_time, matrix_size

if __name__ == '__main__':
    csv_directory = 'matrices_csv'
    os.makedirs(csv_directory, exist_ok=True)

    matrix_dimensions = [50, 100, 150, 200, 250, 300]
    results = []

    for dimensions in matrix_dimensions:
        results.append(run_matrix_multiplication(dimensions))

    elapsed_times, matrix_sizes = zip(*results)

    plt.plot(elapsed_times, matrix_sizes, marker='o')
    plt.title('Tiempo de ejecución vs Dimensión de la Matriz')
    plt.xlabel('Tiempo de ejecución (segundos)')
    plt.ylabel('Dimensión de la Matriz')
    plt.show()
