## Q3a Facilities
# SOLUTION
facility_dict = {}
with open('facilities.txt', 'r') as my_file:
    for line in my_file:
        line = line.rstrip('\n')
        row_details = line.split('\t')
        school = row_details[0]
        room_no = row_details[1]
        capacity = int(row_details[2])
        has_projector = row_details[3]
        key = (school, room_no)
        value = (capacity, has_projector)
        facility_dict[key] = value       

ans = input('\nDo you want to search for a facility? [Y|N] :')
while ans == 'Y':
    school = input('Enter the school [LKCSB|SOE|SOL|SOA|SCIS] :')
    room_no = input('Enter the room number :')
    key = (school, room_no)
    value = facility_dict[key]
    capacity = value[0]
    has_projector = value[1]
    if has_projector == 'yes':
        projector_info = 'has a projector'
    else:
        projector_info = 'does not have a projector'
    print(school, room_no, 'has a capacity of', capacity,'and', projector_info + '.')
    
    ans = input('\nDo you want to search for a facility? [Y|N] :')
    
print('Thanks for using our system!')