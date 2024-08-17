# orm.py

import sqlite3
from typing import List, Optional, Type

class Field:
    def __init__(self, max_length=None, min_length=None, unique=False, auto_now=False):
        self.max_length = max_length
        self.min_length = min_length
        self.unique = unique
        self.auto_now = auto_now

class BaseModel:
    table_name = ''

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def connect(cls):
        raise NotImplementedError("Connect method must be implemented.")
    
    @classmethod
    def create_table(cls):
        conn = cls.connect()
        cursor = conn.cursor()
        columns = []
        for attr, value in cls.__dict__.items():
            if isinstance(value, Field):
                col_type = 'TEXT'
                if isinstance(value, ForeignKey):
                    col_type = 'INTEGER'
                columns.append(f"{attr} {col_type}")
                if value.unique:
                    columns[-1] += " UNIQUE"
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {cls.table_name} (id INTEGER PRIMARY KEY, {', '.join(columns)})")
        conn.commit()
        conn.close()

    @classmethod
    def all(cls) -> List['BaseModel']:
        conn = cls.connect()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {cls.table_name}")
        results = cursor.fetchall()
        conn.close()
        return [cls(**dict(zip([c[0] for c in cursor.description], row))) for row in results]

    @classmethod
    def filter(cls, **kwargs) -> List['BaseModel']:
        conn = cls.connect()
        cursor = conn.cursor()
        query = f"SELECT * FROM {cls.table_name} WHERE " + " AND ".join([f"{k} = ?" for k in kwargs.keys()])
        cursor.execute(query, tuple(kwargs.values()))
        results = cursor.fetchall()
        conn.close()
        return [cls(**dict(zip([c[0] for c in cursor.description], row))) for row in results]

    @classmethod
    def get(cls, **kwargs) -> Optional['BaseModel']:
        conn = cls.connect()
        cursor = conn.cursor()
        query = f"SELECT * FROM {cls.table_name} WHERE " + " AND ".join([f"{k} = ?" for k in kwargs.keys()])
        cursor.execute(query, tuple(kwargs.values()))
        result = cursor.fetchone()
        conn.close()
        if result:
            return cls(**dict(zip([c[0] for c in cursor.description], result)))
        return None

    @classmethod
    def create(cls, **kwargs) -> None:
        conn = cls.connect()
        cursor = conn.cursor()
        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join(['?'] * len(kwargs))
        cursor.execute(f"INSERT INTO {cls.table_name} ({columns}) VALUES ({placeholders})", tuple(kwargs.values()))
        conn.commit()
        conn.close()

    @classmethod
    def update(cls, id: int, **kwargs) -> None:
        conn = cls.connect()
        cursor = conn.cursor()
        set_clause = ', '.join([f"{k} = ?" for k in kwargs.keys()])
        cursor.execute(f"UPDATE {cls.table_name} SET {set_clause} WHERE id = ?", (*kwargs.values(), id))
        conn.commit()
        conn.close()

    @classmethod
    def delete(cls, id: int) -> None:
        conn = cls.connect()
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {cls.table_name} WHERE id = ?", (id,))
        conn.commit()
        conn.close()

class ForeignKey(Field):
    def __init__(self, to: Type['BaseModel'], on_delete='CASCADE'):
        super().__init__()
        self.to = to  # مدل مقصد
        self.on_delete = on_delete  # نوع حذف (CASCADE, SET NULL, etc.)

class SQLiteModel(BaseModel):
    def __init__(self, db_config, **kwargs):
        super().__init__(**kwargs)
        self.db_name = db_config['db_name']

    @classmethod
    def connect(cls):
        return sqlite3.connect(cls().db_name)
