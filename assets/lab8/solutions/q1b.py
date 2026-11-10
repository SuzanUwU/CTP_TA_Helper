## Q1b Substitution Cipher
# SOLUTION 1

def decrypt(my_dict, text):
    
    my_new_dict = {}
    for key in my_dict:
        value = my_dict[key]
        my_new_dict[value] = key
    
    new_text = ''
    for ch in text:
        if ch == ' ':
            new_text += ' '
        else:
            new_ch = my_new_dict[ch]
            new_text += new_ch
    return new_text


# SOLUTION 2
import q1a
def decrypt(my_dict,encrypted_msg):
    decrypt_dict={}

    for k,v in my_dict.items():
        decrypt_dict[v]=k
    
    return q1a.encrypt(decrypt_dict,encrypted_msg)

