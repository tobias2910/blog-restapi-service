import bcrypt
import hmac


def hash_password(hash_password: str):
    '''
    Hash the provided password and store in the password field
    '''
    hash_password = bcrypt.hashpw(
        hash_password.encode('utf-8'), bcrypt.gensalt())
    print(hash_password)


def verify_password(password: str) -> bool:
    hash_password = '$2b$12$Xxzy49Fki44CroHGmrQzA.hfvuunwegSnKoj4.d3lrsO7tgiofdQS'
    print(hmac.compare_digest(bcrypt.hashpw(
        password.encode('utf-8'), hash_password.encode('utf-8')), hash_password.encode('utf-8')))


if __name__ == '__main__':
    verify_password('Elena1990')
