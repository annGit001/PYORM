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

    def get(self,**kwargs):
        key = list(kwargs.keys())[0]
        value = kwargs[key]
        sql = f"""
            SELECT * FROM {self.table} WHERE {key} = ?
        """
        return self.db.execute(sql,(value,)).fetchone()

    def update(self, filters: dict, **kwargs):
        set_ = ", ".join(f"{i}=?" for i in kwargs)
        where_ = " AND ".join(f"{i}=?" for i in filters)

        values = tuple(kwargs.values()) + tuple(filters.values())

        sql = f"""
            UPDATE {self.table}
            SET {set_}
            WHERE {where_}
        """

        self.db.execute(sql, values)

    def delete(self, **filters):
        where_ = " AND ". join(f"{i} = ?" for i in filters)
        values = tuple(filters.values())

        sql = f"""
            DELETE FROM {self.table}
            WHERE {where_}
        """

        self.db.execute(sql, values)

class Model:
    db = Database()

    @classmethod
    def create_table(cls):
        fields = []
        for key,value in cls.__dict__.items():
            if not key.startswith('__') and isinstance(value, str):
                fields.append(f"{key} {value}")
        fields_sql = ", ".join(fields)

        sql = f"""
            CREATE TABLE IF NOT EXISTS {cls.__name__.lower()}s (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            {fields_sql}
        )
        """
        print(sql)
        cls.db.execute(sql)






class User(Model):
    name = "TEXT"
    age = 'INTEGER'
    city = 'TEXT'


User.objects = Manager(User.db, 'users')
# User.create_table()


# User.objects.insert(
#     name = "Anna",
#     age = 25,
#     city = "Yerevan"
# )

print(User.objects.select_all())
# print(User.objects.get(name = "Anna"))
# User.objects.update(
#     {"name": "Anna"},
#     age = 30,
#     city = "Erevan"
# )

# User.objects.delete(city="Erevan")