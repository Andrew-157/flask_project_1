import random
import string


def generate_string(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))


string_51 = generate_string(51)
print(string_51)
