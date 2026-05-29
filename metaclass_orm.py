import sqlite3

class Database:
    def __init__(self, db_name="db.sqlite3"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def execute(self, sql, params=()):
        self.cursor.execute(sql, params)
        self.conn.commit()
        return self.cursor



class Field:
    def __init__(self, column_type, default=None):
        self.column_type = column_type
        self.default = default

    def __repr__(self):
        return f"Field({self.column_type})"



class Manager:
    def __init__(self, db, table):
        self.db = db
        self.table = table


    def insert(self, **kwargs):
        keys = ", ".join(kwargs.keys())
        values = tuple(kwargs.values())
        placeholders = ", ".join(["?"] * len(values))

        sql = f"""
        INSERT INTO {self.table} ({keys})
        VALUES ({placeholders})
        """

        self.db.execute(sql, values)


    def all(self):
        sql = f"SELECT * FROM {self.table}"
        return self.db.execute(sql).fetchall()


    def filter(self, **kwargs):
        where = " AND ".join(f"{k}=?" for k in kwargs)
        values = tuple(kwargs.values())

        sql = f"""
        SELECT * FROM {self.table}
        WHERE {where}
        """

        return self.db.execute(sql, values).fetchall()


    def get(self, **kwargs):
        return self.filter(**kwargs)[0]


    def update(self, filters: dict, values: dict):
        set_ = ", ".join(f"{k}=?" for k in values)
        where_ = " AND ".join(f"{k}=?" for k in filters)

        sql = f"""
        UPDATE {self.table}
        SET {set_}
        WHERE {where_}
        """

        params = tuple(values.values()) + tuple(filters.values())
        self.db.execute(sql, params)


    def delete(self, **filters):
        where = " AND ".join(f"{k}=?" for k in filters)

        sql = f"""
        DELETE FROM {self.table}
        WHERE {where}
        """

        self.db.execute(sql, tuple(filters.values()))



class ModelMeta(type):
    def __new__(cls, name, bases, attrs):

        if name == "BaseModel":
            return super().__new__(cls, name, bases, attrs)

        fields = {}

        for key, value in attrs.items():
            if isinstance(value, Field):
                fields[key] = value

        attrs["_fields"] = fields

        new_cls = super().__new__(cls, name, bases, attrs)

        db = Database()
        new_cls.db = db

        table_name = name.lower() + "s"


        columns = []
        for field_name, field in fields.items():
            columns.append(f"{field_name} {field.column_type}")

        sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            {", ".join(columns)}
        )
        """

        db.execute(sql)

        new_cls.objects = Manager(db, table_name)

        return new_cls



class BaseModel(metaclass=ModelMeta):
    db = Database()



# orinak
class User(BaseModel):
    name = Field("TEXT")
    age = Field("INTEGER")
    city = Field("TEXT")



print(User._fields)

User.objects.insert(
    name="Anna",
    age=25,
    city="Yerevan"
)

print(User.objects.all())

print(User.objects.filter(name="Anna"))

User.objects.update(
    filters={"name": "Anna"},
    values={"age": 30}
)

# User.objects.delete(name="Anna")
