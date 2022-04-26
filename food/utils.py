import random
import string

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))  

def create_new_ref_number():
      return str(random.randint(1000000000, 9999999999))


print(random_string_generator())

print(random_string_generator(size=50))