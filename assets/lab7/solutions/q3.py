# ########################################################################
# Solution 1
# ########################################################################
with open('temperatures.txt') as my_file:
    for line in my_file:
        line = line.rstrip('\n')
        cols = line.split('\t')
        name = cols[0]

        min_temp = cols[1]
        max_temp = cols[1]
        
        for index in range(2, len(cols)):
            if cols[index] < min_temp:
                min_temp = cols[index]
            
            if cols[index] > max_temp:
                max_temp = cols[index]
                
        print(name + ": " + str(min_temp) + ", " + str(max_temp))

# ########################################################################
# Solution 2
# ########################################################################
with open('temperatures.txt', 'r') as my_file:
    for line in my_file:
        temp_list = []
        line = line.rstrip('\n')
        columns = line.split('\t')
        name = columns[0]
        for temp in columns[1:]:
            temp_list.append(temp)
        
        # We can use min() and max() on a list of numbers to find the min and max values.
        print(name + ': ' + str(min(temp_list)) + ', ' + str(max(temp_list)))

# Solution 3
with open('temperatures.txt') as input_file:
    temp_list=[]
    for line in input_file:
        col = line.rstrip().split('\t')
        temp_list.append(col)

for temp in temp_list:
    print(f'{temp[0]}: {min(temp[1:])} {max(temp[1:])}')

