# Q5a: Matrix
# Solution
# ########################################################################
def get_matrix(filename):
    matrix_list = []
    with open(filename, 'r') as my_file:
        for line in my_file:
            num_list_per_row = []
            line = line.rstrip('\n')
            columns = line.split()
            for num in columns:
                num_list_per_row.append(float(num))

            matrix_list.append(num_list_per_row)
        return matrix_list



