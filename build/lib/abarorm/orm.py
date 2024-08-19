import sqlite3
from typing import List, Optional, Dict
import datetime
from .fields import Field, DateTimeField

class ModelMeta(type):
    def __new__(cls, name, bases, dct):
        new_cls = super().__new__(cls, name, bases, dct)
        if 'table_name' in dct and dct['table_name']:  # Check if table_name is defined
            new_cls.create_table()  # Automatically create the table
        return new_cls

class BaseModel(metaclass=ModelMeta):
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
        columns = cls._get_column_definitions(cursor)
        
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {cls.table_name} (id INTEGER PRIMARY KEY, {', '.join(columns)})")
        cls._update_table_structure(cursor)
        conn.commit()
        conn.close()

    @classmethod
    def _get_column_definitions(cls, cursor):
        columns = []
        for attr, field in cls.__dict__.items():
            if isinstance(field, Field):
                col_type = field.field_type
                column_definition = f"{attr} {col_type}"
                if field.unique:
                    column_definition += " UNIQUE"
                if field.null:
                    column_definition += " NULL"
                else:
                    column_definition += " NOT NULL"
                if field.default is not None:
                    if isinstance(field.default, str):
                        column_definition += f" DEFAULT '{field.default}'"
                    else:
                        column_definition += f" DEFAULT {field.default}"
                else:
                    column_definition += " DEFAULT NULL"  # Allow NULL by default to avoid errors
                columns.append(column_definition)
        return columns

    @classmethod
    def _update_table_structure(cls, cursor):
        existing_columns = cls._get_existing_columns(cursor)
        new_columns = [attr for attr in cls.__dict__ if isinstance(cls.__dict__[attr], Field) and attr not in existing_columns]
        
        for column in new_columns:
            field = cls.__dict__[column]
            col_type = field.field_type
            column_definition = f"ALTER TABLE {cls.table_name} ADD COLUMN {column} {col_type}"
            if field.unique:
                column_definition += " UNIQUE"
            if field.null:
                column_definition += " NULL"
            else:
                column_definition += " NOT NULL"
            if field.default is not None:
                if isinstance(field.default, str):
                    column_definition += f" DEFAULT '{field.default}'"
                else:
                    column_definition += f" DEFAULT {field.default}"
            else:
                column_definition += " DEFAULT NULL"  # Allow NULL by default
            cursor.execute(column_definition)
    
    @classmethod
    def _get_existing_columns(cls, cursor):
        cursor.execute(f"PRAGMA table_info({cls.table_name})")
        return {row[1] for row in cursor.fetchall()}

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
        columns = []
        placeholders = []
        values = []
        for attr, field in cls.__dict__.items():
            if isinstance(field, Field):
                if attr in kwargs:
                    columns.append(attr)
                    placeholders.append('?')
                    values.append(kwargs[attr])
                elif isinstance(field, DateTimeField) and field.auto_now:
                    columns.append(attr)
                    placeholders.append('?')
                    values.append(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        cursor.execute(f"INSERT INTO {cls.table_name} ({', '.join(columns)}) VALUES ({', '.join(placeholders)})", tuple(values))
        conn.commit()
        conn.close()

    @classmethod
    def update(cls, id: int, **kwargs) -> None:
        conn = cls.connect()
        cursor = conn.cursor()
        set_clause = ', '.join([f"{k} = ?" for k in kwargs.keys()])
        values = []
        for key, value in kwargs.items():
            field = getattr(cls, key)
            if isinstance(field, DateTimeField) and field.auto_now:
                value = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            values.append(value)
        cursor.execute(f"UPDATE {cls.table_name} SET {set_clause} WHERE id = ?", (*values, id))
        conn.commit()
        conn.close()

    @classmethod
    def delete(cls, id: int) -> None:
        conn = cls.connect()
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {cls.table_name} WHERE id = ?", (id,))
        conn.commit()
        conn.close()

class SQLiteModel(BaseModel):
    def __init__(self, db_config: Dict[str, str], **kwargs):
        super().__init__(**kwargs)
        self.db_name = db_config['db_name']

    @classmethod
    def connect(cls):
        return sqlite3.connect(cls().db_name)
