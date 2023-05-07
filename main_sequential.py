from enum import Enum
import random
import time


class Move(Enum):
    EMPT = 1
    COMP = 2
    PLAY = 3


rows = 6
columns = 7

A = []
for i in range(rows):
    A.append([])
    for j in range(columns):
        A[i].append(Move.EMPT)


def change_whose_move(whose_move):
    if whose_move == Move.COMP:
        return Move.PLAY
    elif whose_move == Move.PLAY:
        return Move.COMP


def is_valid_input(matrix, x):
    return 0 <= x <= columns - 1 and matrix[0][x] == Move.EMPT


def copy_matrix(matrix):
    matrix_copy = []
    for i in range(rows):
        matrix_copy.append([])
        for j in range(columns):
            matrix_copy[i].append(matrix[i][j])
    return matrix_copy


def print_matrix(matrix):
    for i in range(rows):
        for j in range(columns):
            if matrix[i][j] == Move.COMP:
                print("C ", end='')
            elif matrix[i][j] == Move.PLAY:
                print("P ", end='')
            else:
                print("- ", end='')
        print("")


def print_matrices(matrices):
    for matrix in matrices:
        print_matrix(matrix)
        print("")


def are_matrices_the_same(matrix1, matrix2):
    for i in range(rows):
        for j in range(columns):
            if matrix1[i][j] != matrix2[i][j]:
                return False
    return True


def remove_duplicate_matrices(matrices):
    unique_matrices = []
    num_of_matrices = len(matrices)
    for i in range(num_of_matrices - 1):
        found_duplicate = False
        for j in range(num_of_matrices - 1 - i):
            index1 = i
            index2 = i + j + 1
            matrix1 = matrices[index1]
            matrix2 = matrices[index2]
            if are_matrices_the_same(matrix1, matrix2):
                found_duplicate = True
        if not found_duplicate:
            unique_matrices.append(matrix1)
    return unique_matrices


def find_empty_row(matrix, column):
    row = rows - 1
    while matrix[row][column] != Move.EMPT:
        row = row - 1
        if row == -1:
            return -1
    return row


def calculate_child_matrices(matrix, whose_move):

    child_matrices = []

    for j in range(columns):
        i = rows - 1
        changed = False
        while not changed and i >= 0:
            if matrix[i][j] == Move.EMPT:
                matrix_copy = copy_matrix(matrix)
                matrix_copy[i][j] = whose_move
                child_matrices.append(matrix_copy)
                changed = True
            i = i - 1

    return child_matrices


def calculate_child_matrices_deep(matrix, whose_move, depth):

    child_matrices_deep = [matrix]

    for i in range(depth):

        child_matrices = []
        for matrix in child_matrices_deep:
            matrices = calculate_child_matrices(matrix, whose_move)
            for matrix in matrices:
                child_matrices.append(matrix)
        child_matrices_deep = child_matrices

        whose_move = change_whose_move(whose_move)

    child_matrices_deep = remove_duplicate_matrices(child_matrices_deep)

    return child_matrices_deep


def calculate_matrix_quality_final(matrix):

    for i in range(rows):
        count_player = 0
        count_computer = 0
        for j in range(columns):
            if matrix[i][j] == Move.COMP:
                count_computer = count_computer + 1
                count_player = 0
                if count_computer == 4:
                    return 1
            elif matrix[i][j] == Move.PLAY:
                count_player = count_player + 1
                count_computer = 0
                if count_player == 4:
                    return -1
            else:
                count_player = 0
                count_computer = 0

    for j in range(columns):
        count_player = 0
        count_computer = 0
        for i in range(rows):
            if matrix[i][j] == Move.COMP:
                count_computer = count_computer + 1
                count_player = 0
                if count_computer == 4:
                    return 1
            elif matrix[i][j] == Move.PLAY:
                count_player = count_player + 1
                count_computer = 0
                if count_player == 4:
                    return -1
            else:
                count_player = 0
                count_computer = 0

    for i in range(rows):
        for j in range(columns):
            if matrix[i][j] == Move.COMP:
                if i + 1 < rows and j + 1 < columns and matrix[i + 1][j + 1] == Move.COMP:
                    if i + 2 < rows and j + 2 < columns and matrix[i + 2][j + 2] == Move.COMP:
                        if i + 3 < rows and j + 3 < columns and matrix[i + 3][j + 3] == Move.COMP:
                            return 1
            if matrix[i][j] == Move.PLAY:
                if i + 1 < rows and j + 1 < columns and matrix[i + 1][j + 1] == Move.PLAY:
                    if i + 2 < rows and j + 2 < columns and matrix[i + 2][j + 2] == Move.PLAY:
                        if i + 3 < rows and j + 3 < columns and matrix[i + 3][j + 3] == Move.PLAY:
                            return -1
            if matrix[i][j] == Move.COMP:
                if i - 1 > 0 and j + 1 < columns and matrix[i - 1][j + 1] == Move.COMP:
                    if i - 2 > 0 and j + 2 < columns and matrix[i - 2][j + 2] == Move.COMP:
                        if i - 3 > 0 and j + 3 < columns and matrix[i - 3][j + 3] == Move.COMP:
                            return 1
            if matrix[i][j] == Move.PLAY:
                if i - 1 > 0 and j + 1 < columns and matrix[i - 1][j + 1] == Move.PLAY:
                    if i - 2 > 0 and j + 2 < columns and matrix[i - 2][j + 2] == Move.PLAY:
                        if i - 3 > 0 and j + 3 < columns and matrix[i - 3][j + 3] == Move.PLAY:
                            return -1

    return 0


def calculate_matrix_quality(matrix, whose_move, depth):
    child_matrices = calculate_child_matrices(matrix, whose_move)
    sum_of_child_matrices = 0
    num_of_child_matrices = len(child_matrices)
    for child_matrix in child_matrices:
        child_matrix_quality_final = calculate_matrix_quality_final(child_matrix)
        if depth == 0 or child_matrix_quality_final != 0:
            child_matrix_quality = child_matrix_quality_final
        else:
            child_matrix_quality = calculate_matrix_quality(child_matrix, change_whose_move(whose_move), depth - 1)
        if whose_move == Move.COMP and child_matrix_quality == 1:
            return 1
        elif whose_move == Move.PLAY and child_matrix_quality == -1:
            return -1
        else:
            sum_of_child_matrices = sum_of_child_matrices + child_matrix_quality
    return sum_of_child_matrices / num_of_child_matrices


def calculate_comp_move(matrix):

    start_time = time.time()

    child_matrices = calculate_child_matrices(matrix, Move.COMP)

    max_child_matrix_quality = -1
    best_child_matrices = []

    for child_matrix in child_matrices:
        child_matrix_quality = calculate_matrix_quality(child_matrix, Move.PLAY, 3)
        if child_matrix_quality > max_child_matrix_quality:
            max_child_matrix_quality = child_matrix_quality
            best_child_matrices = [child_matrix]
        elif child_matrix_quality == max_child_matrix_quality:
            best_child_matrices.append(child_matrix)

    decided_child_matrix = random.choice(best_child_matrices)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Elapsed time: " + str(elapsed_time))

    return decided_child_matrix


result = 0

print_matrix(A)

while result == 0:

    print("Choose a column ")
    column = int(input()) - 1

    while not is_valid_input(A, column):
        print("Invalid column, choose another ")
        column = int(input()) - 1

    row = find_empty_row(A, column)

    A[row][column] = Move.PLAY
    print("You played")
    print_matrix(A)

    result = calculate_matrix_quality_final(A)
    if result == 1:
        print("You lost :(")
        quit()
    elif result == -1:
        print("You won :)")
        quit()

    A = calculate_comp_move(A)
    print("Computer played")
    print_matrix(A)

    result = calculate_matrix_quality_final(A)
    if result == 1:
        print("You lost :(")
        quit()
    elif result == -1:
        print("You won :)")
        quit()