## Q4 Students and Schools
# SOLUTION

def get_students_by_school(student_school_dict):
    dict_to_return = {}
    
    for student in student_school_dict:
        school = student_school_dict[student]

        if school not in dict_to_return:
            dict_to_return[school] = [student]
        else:
            student_list = dict_to_return[school]
            student_list.append(student)
    return dict_to_return
