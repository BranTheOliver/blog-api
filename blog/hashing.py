from passlib.context import CryptContext


class Hash:
    def __init__(self):
        self.pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash(self, password):
        return self.pwd_ctx.hash(password)

    def verify(self, plain_password, hashed_password):
        return self.pwd_ctx.verify(plain_password, hashed_password)
