## Q6 Employees
# SOLUTION

def create_employee_dictionary(filename):
    
    employees_dict = {}
    with open(filename, 'r') as my_file:
        for line in my_file:
            line = line.rstrip('\n')
            line_details = line.split('\t')
            # extract the id only
            emp_id = int(line_details[0][3:])
            emp_dict = {}
            # extract othe employee details in the rest of the line
            for item in line_details[1:]:
                item_list = item.split(':')
                key = item_list[0]
                value = item_list[1]
                emp_dict[key] = value
            # the value of each employee will be a dictionary containing all his/her details
            employees_dict[emp_id] = emp_dict
    return employees_dict


my_dict = create_employee_dictionary('employees.txt')

# keep prompting until employee exists
continue_search = 'Y'
while continue_search == 'Y':
    
    emp_id = int(input('Enter an employee ID :'))
    
    if emp_id not in my_dict:
        print('Not found!')
    else:
        emp_dict = my_dict[emp_id]
        print('This employee is ' + emp_dict['name'])
        field_name = input("Enter a field name or 'S' to stop :")
        while field_name != 'S':
            if field_name in emp_dict:
                print('The', field_name, 'is', emp_dict[field_name] + '.')
            else:
                print('Not found!')
            field_name = input("Enter a field name or 'S' to stop :")
    
    continue_search = input('\nDo you want to search for another employee? [Y|N] :')

print('Good-bye!')   