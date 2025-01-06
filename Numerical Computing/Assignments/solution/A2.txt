def check_correct_row(k,i,n,matrix):
    row_sum = 0
    for j in range(n):
        if k != j:
            row_sum += abs(matrix[i][j])
            
    if abs(matrix[i][k]) < row_sum:
        return False
    return True


def make_diagonally_dominant(matrix,temp_matrix):
    n = len(matrix)
    i=0
    k=0
    while i<n:
        while k<n:
            check = check_correct_row(i, k, n, matrix)
            if check:
                matrix[i], matrix[k] = matrix[k], matrix[i]
            k+=1
        k=i+1
        i+=1
    if matrix == temp_matrix:
        print(" system cannot be converted into diagonally dominant.")
    else:    
        print("The new matrix is:")
        for row in matrix:
            print(row)
    return matrix
def diagonally_dominant_matrix_check(matrix):
    n = len(matrix)
    for i in range(n):
        row_sum = 0
        for j in range(n):
            if i != j:
                row_sum += abs(matrix[i][j])
        if abs(matrix[i][i]) < row_sum:
            return False
    return True
def input_augmented_matrix(n):
    matrix =[]
    print(f"Enter the augmented matrix:")
    print(f"Each row must have {n + 1} elements.")
    for i in range(n):
        row = input(f"Row {i+1}: ").split()
        if len(row) != n + 1:
            print(f"Each row must have {n + 1} elements.")
            return []
        matrix.append([int(x) for x in row])
    return matrix

def main():
    n = int(input("Enter the size of the matrix (n): "))
    augmented_matrix = input_augmented_matrix(n)
    if augmented_matrix:
        print("The augmented matrix is:")
        for row in augmented_matrix:
            print(row)
        diagonally_dominant = diagonally_dominant_matrix_check(augmented_matrix)
        temp_matrix = [row[:] for row in augmented_matrix]
        if diagonally_dominant:
            print("The matrix is diagonally dominant.")
        else:
            print("The matrix is not diagonally dominant.")
        new_mat= make_diagonally_dominant(augmented_matrix,temp_matrix)
        chek=diagonally_dominant_matrix_check(new_mat)
        if n>1:
            if not chek:
                print("This matrix is not completely diagonally dominant as we can't do it.")
if __name__ == "__main__":
    main()