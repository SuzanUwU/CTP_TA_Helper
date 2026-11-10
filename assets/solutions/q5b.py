# Q5b: Matrix
# Solution
# ########################################################################
import q5a 

def get_matrix_transpose(file_name):
    matrix= q5a.get_matrix(file_name)
    n = len(matrix)
            
    transpose = []
    for i in range(n):
        new_row = []
        for j in range(n):
            new_row.append(matrix[j][i])
        transpose.append(new_row)
    
    return transpose



