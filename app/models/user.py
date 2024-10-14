from app import mongo,bcrypt

class User:
    @staticmethod
    def create(username,password):
        hashed_password=bcrypt.generate_password_hash(password).decode('utf-8')
        user={
            "username":username,
            "password":hashed_password
        }
        return mongo.db.users.insert_one(user)

    @staticmethod
    def find_by_username(username):
        return mongo.db.users.find_one({"username":username})
