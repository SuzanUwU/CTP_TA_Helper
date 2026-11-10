## Q3c 
# SOLUTION

def display_school_facilities_by_capacity(facility_dict, given_school, min_capacity):
    print('\tRoom #\tCap\tProjector?')
    print('\t------\t---\t----------')

    facilities = facility_dict[given_school]
    for facility_info in facilities:
        room_no = facility_info[0]
        capacity = facility_info[1]
        has_projector = facility_info[2]
        if capacity >= min_capacity:
            print('\t' + room_no + '\t' + str(capacity) + '\t' + has_projector)

# read file into a dictionary
facility_dict = {}
with open('facilities.txt', 'r') as my_file:
    for line in my_file:
        line = line.rstrip('\n')
        row_details = line.split('\t')
        school = row_details[0]
        room_no = row_details[1]
        capacity = int(row_details[2])
        has_projector = row_details[3]
        
        facility_info = (room_no, capacity, has_projector)
        
        if school in facility_dict:
            facility_list = facility_dict[school]
            facility_list.append(facility_info)
        else:
            facility_dict[school] = [facility_info]       

ans = input('\nDo you want to search for the facilities within a school? [Y|N]:')
while ans == 'Y':
    school = input('Enter the school [LKCSB|SOE|SOL|SOA|SCIS] :')
    min_capacity = int(input('Enter the minimum capacity you need :'))
    print('The following facilities with a capacity of ' + str(min_capacity) + ' or above are found in ' + school + ' :')
    display_school_facilities_by_capacity(facility_dict, school, min_capacity)
    
    
    ans = input('\nDo you want to search for the facilities within a school? [Y|N]:')
    
print('Good-bye!')
