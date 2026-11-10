## Q2 Prime Numbers
# SOLUTION

def is_prime(num):
    for i in range(2, num):
        if num % i == 0:
            return False
    return True

def create_prime_dict(num_list):
    my_dict = {}
    for num in num_list:
        if is_prime(num):
            my_dict[num] = True
        else:
            my_dict[num] = False
    return my_dict


