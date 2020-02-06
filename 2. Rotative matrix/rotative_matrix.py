import sys


def print_matrix(matrix):
    print(
        '\n'.join([''.join(['{:3}'.format(item) for item in row]) for row in matrix])
    )


def reverse_layer(list, i, j):
    for l in range((j-i+1)//2):
        list[i+l], list[j-l] = list[j-l], list[i+l]
    print(list)


def rotateLayers(r, layers):
    for layer in layers:
        k = len(layer) - r
        l = len(layer)
        k %= int(len(layer))
        reverse_layer(layer, l-k, l-1)
        reverse_layer(layer, 0, l-k-1)
        reverse_layer(layer, 0, l-1)


def matrixRotation(matrix, r):
    m_rows = len(matrix)
    n_columns = len(matrix[0])
    num_rotations = int(min(n_columns, m_rows) // 2)
    layers = [[] for i in range(num_rotations)]
    for i in range(num_rotations):
        top = (n_columns - 1) - 2 * i
        side = (m_rows - 1) - 2 * i
        for j in range(top):
            layers[i].append(matrix[i][i+j])
        for j in range(side):
            layers[i].append(matrix[i+j][i+top])
        for j in range(top):
            layers[i].append(matrix[i+side][i+top-j])
        for j in range(side):
            layers[i].append(matrix[i+side-j][i])
    rotateLayers(r, layers)
    for i in range(num_rotations):
        top = (n_columns - 1) - 2 * i
        side = (m_rows - 1) - 2 * i
        for j in range(top):
            matrix[i][i+j] = layers[i].pop(0)
        for j in range(side):
            matrix[i+j][i+top] = layers[i].pop(0)
        for j in range(top):
            matrix[i+side][i+top-j] = layers[i].pop(0)
        for j in range(side):
            matrix[i+side-j][i] = layers[i].pop(0) 
    print_matrix(matrix)    


if __name__ == "__main__":
    matrix =[
        [1, 2, 3, 4],
        [12, 1, 2, 5],
        [11, 4, 3, 6],
        [10, 9, 8, 7]
    ]
    matrixRotation(matrix, 1)