import random
import string
import json


def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    print("Password is Generating")
    return password



def generate_random_json():

    data = []
    for i in range(20):
        record = {
            'id': i,
            'name': f'User {i}',
            'age': random.randint(18, 65),
            'email': f'user{i}@example.com',
            'phone': f'+91-955-{random.randint(100, 1000)}-{random.randint(100, 1000)}',
            'address': f'{random.randint(1, 100)} GST road, Chennai'
        }
        data.append(record)

    json_data = json.dumps(data, indent=4)
    return json_data


def generate_random():
    rand_int = random.randint(1, 100)
    return rand_int

