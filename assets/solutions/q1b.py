# Q1b Reading Files
# Solution
# ########################################################################
def print_alternate_columns(file_name):
    with open(file_name, 'r') as my_file:
        line_number = 0
        for line in my_file:
            line = line.rstrip('\n')
            cols = line.split('&')
            col_number = 0
            
            print(cols[0], end='')
            for index in range(1, len(cols)):
                if index % 2 == 0:
                    print('&' + cols[index], end='')
            print()





