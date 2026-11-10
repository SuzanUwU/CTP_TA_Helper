## Q5a Word Counts
# SOLUTION

def count_words_in_file(filename):
    dict_to_return = {}
    with open(filename, 'r') as my_file:
        for line in my_file:
            line = line.rstrip('\n')
            line = line.lower()
            line_words = line.split()
            for word in line_words:
                if word in dict_to_return:
                    dict_to_return[word] = dict_to_return[word] + 1
                else:
                    dict_to_return[word] = 1
    return dict_to_return

