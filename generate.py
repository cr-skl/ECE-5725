import random

def generate_matrix(size):
    matrix = [[0] * size[1] for _ in range(size[0])]

    # Place a 5 either against the edge or surrounded by 1
    edge_placement = random.choice([True, False])

    if edge_placement:
        edge = random.choice(['top', 'bottom', 'left', 'right'])
        if edge == 'top':
            row, col = 0, random.randint(1, size[1] - 2)
        elif edge == 'bottom':
            row, col = size[0] - 1, random.randint(1, size[1] - 2)
        elif edge == 'left':
            row, col = random.randint(1, size[0] - 2), 0
        else:  # edge == 'right'
            row, col = random.randint(1, size[0] - 2), size[1] - 1
    else:
        row, col = random.randint(1, size[0] - 2), random.randint(1, size[1] - 2)
        matrix[row][col] = 5
        matrix[row - 1][col] = matrix[row + 1][col] = matrix[row][col - 1] = matrix[row][col + 1] = 1
        return matrix

    matrix[row][col] = 5

    # Fill the rest of the matrix
    for i in range(size[0]):
        for j in range(size[1]):
            if matrix[i][j] == 0:
                rand_num = random.uniform(0, 1)
                if rand_num <= 0.3:
                    matrix[i][j] = 1
                elif 0.3 < rand_num <= 0.5:
                    matrix[i][j] = 3

    return matrix

def print_matrix(matrix):
    for row in matrix:
        print(row)
        
if __name__ == '__main__':
    # Specify the size of the matrix
    matrix_size = (13, 19)

    # Generate the matrix
    generated_matrix = generate_matrix(matrix_size)

    # Print the generated matrix
    print_matrix(generated_matrix)
