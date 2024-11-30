import sqlite3
from typing import List, Optional, Dict
import datetime
from .fields import Field, DateTimeField, DecimalField, TimeField, DateField, CharField, ForeignKey

class ModelMeta(type):
    def __new__(cls, name, bases, dct):
        new_cls = super().__new__(cls, name, bases, dct)
        if not hasattr(new_cls.Meta, 'table_name') or not new_cls.Meta.table_name:
            new_cls.table_name = name.lower()  # Automatically set table_name from model class name
        else:
            new_cls.table_name = new_cls.Meta.table_name  # Override with Meta.table_name if provided

        if hasattr(new_cls.Meta, 'db_config') and new_cls.Meta.db_config:
            new_cls.create_table()  # Automatically create the table if db_config is present
        return new_cls


class BaseModel(metaclass=ModelMeta):
    table_name = ''
    
    class QuerySet:
        def __init__(self, results):
            self.results = results

        def count(self) -> int:
            """Returns the number of results."""
            return len(self.results)

        def to_dict(self) -> List[Dict]:
            """Returns the results as a list of dictionaries."""
            return [obj.__dict__ for obj in self.results]
        def __repr__(self):
            """Returns a string representation of the QuerySet."""
            # If there are results, show the first 3 as a sample
            sample = self.to_dict()[:3]  # Show first 3 items for example
            return f"<QuerySet(count={self.count()}, first_3_fitst_items={sample})>"  

    
    def __repr__(self):
        # Get all field names and their corresponding values
        field_values = {attr: getattr(self, attr) for attr in self.__class__.__dict__ if isinstance(self.__class__.__dict__[attr], Field)}
        # Format the dictionary into a readable string
        return f"<{self.__class__.__name__} {field_values}>"
    
    class Meta:
        db_config = {}  # Default empty config, should be overridden in the actual model

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def connect(cls):
        config = getattr(cls.Meta, 'db_config', None)
        if not config or 'db_name' not in config:
            raise ValueError("Database configuration 'db_name' is missing in Meta class")
        return sqlite3.connect(config['db_name'])

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
                if isinstance(field, DecimalField):
                    col_type += f"({field.max_digits}, {field.decimal_places})"
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
            if isinstance(field, DecimalField):
                col_type += f"({field.max_digits}, {field.decimal_places})"

            # Start with default constraints
            column_definition = f"ALTER TABLE {cls.table_name} ADD COLUMN {column} {col_type}"
            column_definition += " NULL" if field.null else " NOT NULL"
            
            if field.unique:
                column_definition += " UNIQUE"
            if field.default is not None:
                if isinstance(field.default, str):
                    column_definition += f" DEFAULT '{field.default}'"
                else:
                    column_definition += f" DEFAULT {field.default}"
            else:
                column_definition += " DEFAULT NULL"

            try:
                # Try adding the column with the defined constraints
                cursor.execute(column_definition)
            except sqlite3.OperationalError as e:
                # If NOT NULL constraint fails, attempt with NULL
                if "NOT NULL" in str(e):
                    print(f"Adding column {column} with NULL temporarily due to NOT NULL constraint failure.")
                    cursor.execute(f"ALTER TABLE {cls.table_name} ADD COLUMN {column} {col_type} NULL")
                    # Optionally, log or mark this field for future fixing of constraints.
                else:
                    raise e  # Reraise for other exceptions
    
    @classmethod
    def _get_existing_columns(cls, cursor):
        cursor.execute(f"PRAGMA table_info({cls.table_name})")
        return {row[1] for row in cursor.fetchall()}
    
    @classmethod
    def all(cls, order_by: Optional[str] = None) -> List['BaseModel']:
        conn = cls.connect()
        cursor = conn.cursor()
        query = f"SELECT * FROM {cls.table_name}"
        if order_by:
            query += f" ORDER BY {order_by}"
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return cls.QuerySet([cls(**dict(zip([c[0] for c in cursor.description], row))) for row in results])

    @classmethod
    def filter(cls, order_by: Optional[str] = None, **kwargs) -> List['BaseModel']:
        conn = cls.connect()
        cursor = conn.cursor()

        conditions = []
        values = []
        for key, value in kwargs.items():
            if key.endswith("__gte"):
                conditions.append(f"{key[:-5]} >= ?")
            elif key.endswith("__lte"):
                conditions.append(f"{key[:-5]} <= ?")
            else:
                conditions.append(f"{key} = ?")
            values.append(value)

        query = f"SELECT * FROM {cls.table_name} WHERE " + " AND ".join(conditions)
        if order_by:
            query += f" ORDER BY {order_by.lstrip('-')} {'DESC' if order_by.startswith('-') else 'ASC'}"

        cursor.execute(query, tuple(values))
        results = cursor.fetchall()
        conn.close()

        return cls.QuerySet([cls(**dict(zip([c[0] for c in cursor.description], row))) for row in results])
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
                if isinstance(field, ForeignKey):
                    # Check if the category exists if the value is an integer
                    if isinstance(kwargs[attr], int):
                        related_instance = field.to.get(id=kwargs[attr])
                        if not related_instance:
                            raise ValueError(f"Related {field.to.__name__} with ID {kwargs[attr]} does not exist.")
                    
                    # If the value is an instance of the related model, extract the ID
                    elif isinstance(kwargs[attr], field.to):
                        values.append(kwargs[attr].id)  # Assuming the ID attribute is called `id`
                    else:
                        raise ValueError(f"Invalid value for foreign key {attr}. Must be an integer ID or instance of {field.to.__name__}.")
                
                if attr in kwargs:
                    columns.append(attr)
                    placeholders.append('?')
                    values.append(kwargs[attr])
                elif isinstance(field, DateField) and field.auto_now:
                    columns.append(attr)
                    placeholders.append('?')  # Use '?' for SQLite placeholder
                    values.append(datetime.datetime.now().strftime('%Y-%m-%d'))
                elif isinstance(field, DateField) and field.auto_now_add:
                    columns.append(attr)
                    placeholders.append('?')  # Use '?' for SQLite placeholder
                    values.append(datetime.datetime.now().strftime('%Y-%m-%d'))
                elif isinstance(field, DateTimeField) and field.auto_now:
                    columns.append(attr)
                    placeholders.append('?')  # Use '?' for SQLite placeholder
                    values.append(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                elif isinstance(field, DateTimeField) and field.auto_now_add:
                    columns.append(attr)
                    placeholders.append('?')  # Use '?' for SQLite placeholder
                    values.append(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    
                    
        cursor.execute(f"INSERT INTO {cls.table_name} ({', '.join(columns)}) VALUES ({', '.join(placeholders)})", tuple(values))
        conn.commit()
        conn.close()
        return True  # Return True on successful creation

    def save(self):
        if hasattr(self, 'id') and self.id:
            data = self.__dict__.copy()
            data.pop('id', None)
            self.__class__.update(self.id, **data)
        else:
            self.__class__.create(**self.__dict__)

    @classmethod
    def update(cls, id: int, **kwargs) -> bool:
        conn = cls.connect()
        cursor = conn.cursor()

        set_clause = ', '.join([f"{k} = ?" for k in kwargs.keys()])
        values = []
        for key, value in kwargs.items():
            field = getattr(cls, key)
            if isinstance(field, DateTimeField) and field.auto_now:
                value = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if isinstance(field, DateField) and field.auto_now:
                value = datetime.datetime.now().strftime('%Y-%m-%d')
            values.append(value)
        cursor.execute(f"UPDATE {cls.table_name} SET {set_clause} WHERE id = ?", (*values, id))
        conn.commit()
        conn.close()

        return True
        

    @classmethod
    def delete(cls, id: int) -> None:
        conn = cls.connect()
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {cls.table_name} WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return True
        

class SQLiteModel(BaseModel):
    class Meta:
        db_config = {}  # To be overridden by the model class
