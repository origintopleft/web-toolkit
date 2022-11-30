import random
import string

str_guestcheck_token_characters = string.ascii_uppercase + string.digits

def init_error():
    # stub
    return ''.join([random.choice(str_guestcheck_token_characters) for i in range(30)])