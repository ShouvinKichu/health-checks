import random
import string


def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation

    password = ""

    for _ in range(length):
        password += random.choice(characters)

    return password


length = int(input("Enter password length: "))

print("\nGenerated Password:")
print(generate_password(length))