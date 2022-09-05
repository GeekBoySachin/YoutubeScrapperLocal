import os


class Credentials:
    def __init__(self):
        self.sql_host = os.getenv("SQL_HOST")
        self.sql_user = os.getenv("SQL_USER")
        self.sql_pass = os.getenv("SQL_PASSWORD")
        self.mongo_uri = os.getenv("MONGO_URI")

    def get_sql_host(self):
        return self.sql_host

    def get_sql_user(self):
        return self.sql_user

    def get_sql_password(self):
        return self.sql_pass

    def get_mongo_uri(self):
        return self.mongo_uri


if __name__ == "__main__":
    obj = Credentials()
    print(obj.get_sql_user())
    print(obj.get_sql_password())
    print(obj.get_mongo_uri())