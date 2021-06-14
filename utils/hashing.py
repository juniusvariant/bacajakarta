from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"])

class Hash():
    def bcrypt(password: str):
        hashedPassword = pwd_cxt.hash(password)
        return hashedPassword

    def verify(plain_password: str, hashed_password: str):
        return pwd_cxt.verify(plain_password, hashed_password)