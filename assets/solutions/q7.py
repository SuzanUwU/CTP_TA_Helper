# Q7
# Solution
# ########################################################################
import random

special_characters =  ",'!."

def scramble(word):
    if len(word) <= 3:
        return word
    middle_word = word[1:len(word)-1]
    my_list = list(middle_word)
    random.shuffle(my_list)
    scrambled_midle_word = ''.join(my_list)
    result = word[0] + scrambled_midle_word + word[len(word)-1]
    return result


with open('talk.txt','r') as my_file:
    for line in my_file:
        line = line.rstrip('\n')
        words = line.split()
        scrambled_line = []
        for word in words:
            last_char = word[len(word)-1]
            if last_char in special_characters:
                word = word[0:len(word)-1]
                scrambled_word = scramble(word)
                full_scrambled_word = scrambled_word + last_char
            else:
                full_scrambled_word = scramble(word)
            scrambled_line.append(full_scrambled_word)  
        for word in scrambled_line:
            print(word, end = ' ' )
        print('\n')