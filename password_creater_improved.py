import os
import hashlib
import secrets
import system
from Crypto.Protocol.KDF import PBKDF2
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

# Constants 
PBKDF2_ITERATIONS = 100000
SALT_SIZE = 16
KEY_SIZE = 32

# Function to generate a random password
def generate_password(length, charset):
    return ''.join(secrets.choice(charset) for _ in range(length))

# Function to derive a secure key using PBKDF2
def derive_key(password, salt):
    return PBKDF2(password.encode('utf-8'), salt, dkLen=KEY_SIZE, count=PBKDF2_ITERATIONS)

# Function to validate the master password
def validate_master_password(stored_hash, master_password, salt):
    key = derive_key(master_password, salt)
    return stored_hash == key

# Function to set file permissions
def set_file_permissions(filepath, permissions):
    os.chmod(filepath, permissions)

# Function to read the saved salt and key hash
def read_key_storage(filepath):
    try:
        with open(filepath, 'rb') as f:
            salt = f.read(SALT_SIZE)
            stored_hash = f.read(KEY_SIZE)
            return salt, stored_hash
    except FileNotFoundError:
        print("Error: Key storage file not found.")
        return None, None
    except Exception as e:
        print(f'Error reading key storage: {e}')
        return None, None

# Function to validate input characters
def validate_charset(charset):
    if not charset or any(not c.isprintable() for c in charset):
        raise ValueError('Invalid character set provided. All characters must be printable.')
    return True

# Main function
if __name__ == '\__main__':
    MASTER_PASSWORD = input('Enter master password: ')
    filepath = 'key_storage.bin'
    salt, stored_hash = read_key_storage(filepath)

    if salt and stored_hash:
        if validate_master_password(stored_hash, MASTER_PASSWORD, salt):
            print('Master password is valid.')
        else:
            print('Invalid master password.')
            exit(1)

    charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()'
    validate_charset(charset)  # Validation of charset
    password_length = int(input('Enter desired password length: '))
    password = generate_password(password_length, charset)
    print(f'Generated password: {password}')  # Display generated password
    set_file_permissions(filepath, 0o600)  # Set file permissions to read/write for the owner only
    
