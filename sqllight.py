import sqlite3
class Database:
    def __init__(self, db_name = 'db.sqlite3'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def execute(self, sql, params = ()):
        self.cursor.execute(sql, params)
        self.conn.commit()
        return self.cursor

class Manager:
    def __init__(self,db,table):
        self.db = db
        self.table = table

    def insert(self, **kwargs):
        keys = ",".join(kwargs.keys())
        values = tuple(kwargs.values())
        placeholders = ",".join(["?"]*len(values))
        sql = f"""
            INSERT INTO {self.table}({keys}) VALUES ({placeholders})
        """
        self.db.execute(sql, values)

    def select_all(self):
        return self.db.execute(f"SELECT * FROM {self.table}").fetchall()


class Model:
    db = Database()


class User(Model):
    pass



User.objects = Manager(User.db, 'user')

User.db.execute("""
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    age INTEGER
)
""")

# user = Manager(db, 'user')

# user.insert(name='Anna', age=25)


# db.execute("""
#     INSERT INTO user (name, age) VALUES (?, ?)
# """,("Anna", 24))

# rows = db.execute("""
#     Select * from user
# """).fetchall()
# print(rows)
# print(user.select_all())


User.objects.insert(
    name="Anna",
    age=25
)

print(User.objects.select_all())