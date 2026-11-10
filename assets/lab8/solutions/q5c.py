## Q5c Word Counts
# SOLUTION
from q5a import count_words_in_file

file = 'spam_sms.txt'
my_dict = count_words_in_file(file)

top_words = []
for i in range(10):
    
    top_word = ''
    max_freq = 0
    for word in my_dict:
        frequency = my_dict[word]
        my_tuple = (word, frequency)
        if my_tuple not in top_words and frequency > max_freq:
            max_freq = frequency
            top_word = word
    top_words.append( (top_word, max_freq) )

print(top_words)