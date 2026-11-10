## Q1a Substitution Cipher
# SOLUTION

def encrypt(cipher_dict, message):
    encrypted_message = ''
    for ch in message:
        if ch != ' ':
            encrypted_ch = cipher_dict[ch]
        else:
            encrypted_ch = ch
        encrypted_message += encrypted_ch
        
    return encrypted_message









        
