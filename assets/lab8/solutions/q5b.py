## Q5b Word Counts
# SOLUTION
from q5a import count_words_in_file

file = 'spam_sms.txt'
my_dict = count_words_in_file(file)

for key in my_dict:
    frequency = my_dict[key]
    if len(key) >= 4 and frequency > 50:
        print(key + " : " + str(frequency))
        
