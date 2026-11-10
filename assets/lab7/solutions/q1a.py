# Q1 Reading Files
# solution
# ########################################################################
def print_alternate_lines(filename):
    with open(filename, 'r') as my_file:
        count = 0
        for line in my_file:
            line = line.rstrip('\n')
            if count % 2 == 0:
                print(line)
            count += 1




