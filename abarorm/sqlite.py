import sqlite3
from typing import List, Optional, Dict
import datetime
from datetime import date
from .fields.sqlite import Field, DateTimeField, DecimalField, TimeField, DateField, CharField, ForeignKey, EmailField, URLField


class RelatedManager:
    """Manager for handling related objects from ForeignKey"""
    
    def __init__(self, model, field_name, instance_id):
        self.model = model
        self.field_name = field_name
        self.instance_id = instance_id

    def all(self):
        """Get all related objects"""
        return self.model.filter(**{self.field_name: self.instance_id})

    def filter(self, **kwargs):
        """Filter related objects"""
        return self.model.filter(**{self.field_name: self.instance_id, **kwargs})

    def first(self):
        """Get first related object"""
        qs = self.all()
        return qs.first() if qs.exists() else None

    def last(self):
        """Get last related object"""
        qs = self.all()
        return qs.last() if qs.exists() else None

    def count(self):
        """Count related objects"""
        return self.all().count()
    
    def to_dict(self) -> List[Dict]:
        """Convert related objects to list of dicts"""
        return self.all().to_dict()


class ModelMeta(type):
    """Metaclass for automatic table creation and related_name setup"""
    
    def __new__(cls, name, bases, dct):
        new_cls = super().__new__(cls, name, bases, dct)

        # Set table name
        if not hasattr(new_cls.Meta, 'table_name') or not new_cls.Meta.table_name:
            new_cls.table_name = name.lower()
        else:
            new_cls.table_name = new_cls.Meta.table_name

        # Setup related_name for ForeignKeys
        for attr, field in dct.items():
            if isinstance(field, ForeignKey) and field.related_name:
                def related_manager(self, _model=new_cls, _field=attr):
                    return RelatedManager(_model, _field, self.id)
                setattr(field.to, field.related_name, property(related_manager))

        # Auto-create table if db_config exists
        if hasattr(new_cls.Meta, 'db_config') and new_cls.Meta.db_config:
            new_cls.create_table()

        return new_cls


class BaseModel(metaclass=ModelMeta):
    """Base model class for SQLite ORM"""
    
    table_name = ''
    
    class QuerySet:
        """QuerySet for handling query results"""
        
        def __init__(self, results, total_count, page, page_size):
            self.results = results
            self.total_count = total_count
            self.page = page
            self.page_size = page_size
        
        def filter(self, **kwargs) -> 'QuerySet':
            """Filter QuerySet results in-memory"""
            if not kwargs:
                raise ValueError("At least one filter must be provided")

            filtered_results = []

            for obj in self.results:
                match = True
                for key, value in kwargs.items():
                    if '__' in key:
                        field_name, op = key.split('__', 1)
                        field_value = getattr(obj, field_name, None)
                        
                        if op == 'gte' and not (field_value >= value):
                            match = False
                            break
                        elif op == 'lte' and not (field_value <= value):
                            match = False
                            break
                        elif op == 'gt' and not (field_value > value):
                            match = False
                            break
                        elif op == 'lt' and not (field_value < value):
                            match = False
                            break
                        elif op == 'exact' and not (field_value == value):
                            match = False
                            break
                        else:
                            raise ValueError(f"Unsupported filter operator: {op}")
                    else:
                        if getattr(obj, key, None) != value:
                            match = False
                            break

                if match:
                    filtered_results.append(obj)

            return self.__class__(filtered_results, len(filtered_results), self.page, self.page_size)
        
        def count(self) -> int:
            """Count results"""
            return len(self.results)

        def to_dict(self) -> List[Dict]:
            """Convert results to list of dictionaries"""
            return [obj.__dict__ for obj in self.results]
        
        def __repr__(self):
            """String representation"""
            sample = self.to_dict()[:3]
            return f"<QuerySet(count={self.count()}, first_3_items={sample})>"
        
        def order_by(self, field: str):
            """Order results by field"""
            reverse = field.startswith('-')
            field_name = field.lstrip('-')
            
            try:
                sorted_results = sorted(
                    self.results,
                    key=lambda obj: getattr(obj, field_name),
                    reverse=reverse
                )
            except AttributeError:
                raise ValueError(f"Field '{field_name}' does not exist")
            
            return self.__class__(sorted_results, self.total_count, self.page, self.page_size)
        
        def first(self):
            """Get first result"""
            return self.results[0] if self.results else None

        def last(self):
            """Get last result"""
            return self.results[-1] if self.results else None
        
        def exists(self) -> bool:
            """Check if results exist"""
            return bool(self.results)

        def paginate(self, page: int, page_size: int):
            """Paginate results"""
            if page < 1:
                raise ValueError("Page number must be >= 1")
            if page_size < 1:
                raise ValueError("Page size must be >= 1")
            
            offset = (page - 1) * page_size
            paginated_results = self.results[offset:offset + page_size]
            return self.__class__(paginated_results, self.total_count, page, page_size)
        
        def contains(self, **kwargs) -> 'QuerySet':
            """Case-insensitive contains search"""
            if not kwargs:
                raise ValueError("At least one field must be provided")

            filtered_results = []

            for obj in self.results:
                match = True
                for field, value in kwargs.items():
                    field_value = getattr(obj, field, None)
                    
                    if isinstance(field_value, str):
                        if str(value).lower() not in field_value.lower():
                            match = False
                            break
                    elif isinstance(field_value, (int, float)):
                        if str(value) not in str(field_value):
                            match = False
                            break
                    elif isinstance(field_value, (datetime.datetime, datetime.date)):
                        if str(value) not in field_value.strftime('%Y-%m-%d'):
                            match = False
                            break
                    elif field_value != value:
                        match = False
                        break

                if match:
                    filtered_results.append(obj)

            return self.__class__(filtered_results, len(filtered_results), self.page, self.page_size)

    def __repr__(self):
        """String representation of model instance"""
        field_values = {
            attr: getattr(self, attr, None) 
            for attr in self.__class__.__dict__ 
            if isinstance(self.__class__.__dict__[attr], Field)
        }
        return f"<{self.__class__.__name__} {field_values}>"
    
    class Meta:
        db_config = {}

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def connect(cls):
        """Create database connection"""
        config = getattr(cls.Meta, 'db_config', None)
        if not config or 'db_name' not in config:
            raise ValueError("Database configuration 'db_name' is missing in Meta class")
        
        conn = sqlite3.connect(config['db_name'])
        # Enable foreign key support in SQLite
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    @classmethod
    def create_table(cls):
        """Create database table with foreign key constraints"""
        conn = cls.connect()
        try:
            cursor = conn.cursor()
            columns = cls._get_column_definitions()
            foreign_keys = cls._get_foreign_key_constraints()
            
            # Build CREATE TABLE statement
            table_parts = [f"id INTEGER PRIMARY KEY AUTOINCREMENT"]
            table_parts.extend(columns)
            table_parts.extend(foreign_keys)
            
            create_sql = f"CREATE TABLE IF NOT EXISTS {cls.table_name} ({', '.join(table_parts)})"
            cursor.execute(create_sql)
            
            # Update existing table structure
            cls._update_table_structure(cursor)
            
            conn.commit()
        finally:
            conn.close()

    @classmethod
    def _get_column_definitions(cls):
        """Generate column definitions for CREATE TABLE"""
        columns = []
        
        for attr, field in cls.__dict__.items():
            if not isinstance(field, Field):
                continue
            
            # Skip ForeignKey columns (they're regular INTEGER with constraints)
            col_type = field.field_type
            
            if isinstance(field, DecimalField):
                # Note: SQLite doesn't support DECIMAL(m,n) syntax, stores as REAL
                pass
            
            column_def = f"{attr} {col_type}"
            
            if field.unique:
                column_def += " UNIQUE"
            
            if not field.null:
                column_def += " NOT NULL"
            
            if field.default is not None:
                if isinstance(field.default, str):
                    column_def += f" DEFAULT '{field.default}'"
                else:
                    column_def += f" DEFAULT {field.default}"
            
            columns.append(column_def)
        
        return columns

    @classmethod
    def _get_foreign_key_constraints(cls):
        """Generate FOREIGN KEY constraints"""
        constraints = []
        
        for attr, field in cls.__dict__.items():
            if isinstance(field, ForeignKey):
                constraints.append(field.get_constraint(attr))
        
        return constraints

    @classmethod
    def _update_table_structure(cls, cursor):
        """Add new columns to existing table"""
        existing_columns = cls._get_existing_columns(cursor)
        new_columns = [
            attr for attr in cls.__dict__ 
            if isinstance(cls.__dict__[attr], Field) and attr not in existing_columns
        ]

        for column in new_columns:
            field = cls.__dict__[column]
            col_type = field.field_type
            
            column_def = f"ALTER TABLE {cls.table_name} ADD COLUMN {column} {col_type}"
            
            # For new columns, always allow NULL initially to avoid errors
            column_def += " NULL"
            
            if field.default is not None:
                if isinstance(field.default, str):
                    column_def += f" DEFAULT '{field.default}'"
                else:
                    column_def += f" DEFAULT {field.default}"

            try:
                cursor.execute(column_def)
            except sqlite3.OperationalError as e:
                print(f"Warning: Could not add column {column}: {e}")
    
    @classmethod
    def _get_existing_columns(cls, cursor):
        """Get existing columns from table"""
        cursor.execute(f"PRAGMA table_info({cls.table_name})")
        return {row[1] for row in cursor.fetchall()}
    
    @classmethod
    def _get_valid_fields(cls):
        """Cache valid field names for performance"""
        if not hasattr(cls, '_valid_fields_cache'):
            cls._valid_fields_cache = {
                attr for attr, field in cls.__dict__.items() 
                if isinstance(field, Field)
            }
        return cls._valid_fields_cache
    
    @classmethod
    def _validate_and_convert_values(cls, **kwargs):
        """Validate and convert field values using field validators"""
        validated = {}
        
        for attr, field in cls.__dict__.items():
            if not isinstance(field, Field):
                continue
            
            # Handle ForeignKey
            if isinstance(field, ForeignKey):
                if attr in kwargs:
                    try:
                        validated[attr] = field.validate(kwargs[attr])
                    except ValueError as e:
                        raise ValueError(f"Validation error for field '{attr}': {e}")
                continue
            
            # Handle regular fields
            if attr in kwargs:
                # Apply field validation if method exists
                if hasattr(field, 'validate'):
                    try:
                        validated[attr] = field.validate(kwargs[attr])
                    except ValueError as e:
                        raise ValueError(f"Validation error for field '{attr}': {e}")
                else:
                    validated[attr] = kwargs[attr]
            
            # Handle auto_now and auto_now_add
            elif isinstance(field, (DateField, DateTimeField)):
                if field.auto_now or field.auto_now_add:
                    if isinstance(field, DateField):
                        validated[attr] = datetime.datetime.now().date().isoformat()
                    else:
                        validated[attr] = datetime.datetime.now().isoformat()
        
        return validated
    
    @classmethod
    def all(cls, order_by: Optional[str] = None) -> 'QuerySet':
        """Get all records"""
        conn = cls.connect()
        try:
            cursor = conn.cursor()
            query = f"SELECT * FROM {cls.table_name}"
            
            if order_by:
                field_name = order_by.lstrip('-')
                valid_fields = cls._get_valid_fields()
                if field_name not in valid_fields:
                    raise ValueError(f"Invalid field name for ordering: {field_name}")
                
                direction = "DESC" if order_by.startswith('-') else "ASC"
                query += f" ORDER BY {field_name} {direction}"
            
            cursor.execute(query)
            results = cursor.fetchall()
            
            return cls.QuerySet(
                [cls(**dict(zip([c[0] for c in cursor.description], row))) for row in results],
                len(results),
                page=1,
                page_size=len(results)
            )
        finally:
            conn.close()

    @classmethod
    def filter(cls, **kwargs) -> 'QuerySet':
        """Filter records with various operators"""
        if not kwargs:
            return cls.all()
        
        conditions = []
        values = []
        valid_fields = cls._get_valid_fields()

        for key, value in kwargs.items():
            base_key = key
            operator = "="
            
            if key.endswith("__gte"):
                base_key = key[:-5]
                operator = ">="
            elif key.endswith("__lte"):
                base_key = key[:-5]
                operator = "<="
            elif key.endswith("__gt"):
                base_key = key[:-4]
                operator = ">"
            elif key.endswith("__lt"):
                base_key = key[:-4]
                operator = "<"
            elif key.endswith("__ne"):
                base_key = key[:-4]
                operator = "!="
            elif key.endswith("__contains"):
                base_key = key[:-10]
                if base_key not in valid_fields:
                    raise ValueError(f"Invalid field name: {base_key}")
                conditions.append(f"{base_key} LIKE ?")
                values.append(f"%{value}%")
                continue
            elif key.endswith("__icontains"):
                base_key = key[:-11]
                if base_key not in valid_fields:
                    raise ValueError(f"Invalid field name: {base_key}")
                conditions.append(f"LOWER({base_key}) LIKE LOWER(?)")
                values.append(f"%{value}%")
                continue
            elif key.endswith("__in"):
                base_key = key[:-4]
                if not isinstance(value, (list, tuple)):
                    raise ValueError(f"Value for {key} must be a list or tuple")
                if base_key not in valid_fields:
                    raise ValueError(f"Invalid field name: {base_key}")
                placeholders = ", ".join(["?" for _ in value])
                conditions.append(f"{base_key} IN ({placeholders})")
                values.extend(value)
                continue
            
            if base_key not in valid_fields:
                raise ValueError(f"Invalid field name: {base_key}")
            
            conditions.append(f"{base_key} {operator} ?")
            values.append(value)

        query = f"SELECT * FROM {cls.table_name} WHERE " + " AND ".join(conditions)
        
        conn = cls.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(query, tuple(values))
            results = cursor.fetchall()
            
            return cls.QuerySet(
                [cls(**dict(zip([c[0] for c in cursor.description], row))) for row in results],
                len(results),
                page=1,
                page_size=len(results)
            )
        finally:
            conn.close()

    @classmethod
    def get(cls, **kwargs) -> Optional['BaseModel']:
        """Get single record"""
        if not kwargs:
            raise ValueError("At least one filter must be provided")
        
        valid_fields = cls._get_valid_fields()
        
        for key in kwargs.keys():
            if key not in valid_fields:
                raise ValueError(f"Invalid field name: {key}")
        
        conn = cls.connect()
        try:
            cursor = conn.cursor()
            query = f"SELECT * FROM {cls.table_name} WHERE " + " AND ".join([f"{k} = ?" for k in kwargs.keys()])
            cursor.execute(query, tuple(kwargs.values()))
            result = cursor.fetchone()
            
            if result:
                return cls(**dict(zip([c[0] for c in cursor.description], result)))
            return None
        finally:
            conn.close()

    @classmethod
    def create(cls, **kwargs) -> int:
        """Create new record with validation"""
        # Validate and convert all values
        validated_data = cls._validate_and_convert_values(**kwargs)
        
        conn = cls.connect()
        try:
            cursor = conn.cursor()
            columns = list(validated_data.keys())
            placeholders = ['?' for _ in columns]
            values = list(validated_data.values())
            
            query = f"INSERT INTO {cls.table_name} ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"
            cursor.execute(query, tuple(values))
            
            new_id = cursor.lastrowid
            conn.commit()
            return new_id
        finally:
            conn.close()
    
    @classmethod
    def bulk_create(cls, records: list) -> int:
        """Bulk create records with validation"""
        if not records:
            raise ValueError("The records list is empty")
        
        conn = cls.connect()
        try:
            cursor = conn.cursor()
            all_values = []
            
            for record in records:
                validated_data = cls._validate_and_convert_values(**record)
                all_values.append(tuple(validated_data.values()))
            
            # Use columns from first validated record
            first_validated = cls._validate_and_convert_values(**records[0])
            columns = list(first_validated.keys())
            placeholders = ", ".join(["?" for _ in columns])
            query = f"INSERT INTO {cls.table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            
            cursor.executemany(query, all_values)
            conn.commit()
            return len(all_values)
        finally:
            conn.close()

    def save(self):
        """Save instance (insert or update)"""
        if hasattr(self, 'id') and self.id:
            data = self.__dict__.copy()
            data.pop('id', None)
            try:
                self.__class__.update(self.id, **data)
            except ValueError as e:
                raise ValueError(f"Cannot save: {e}")
        else:
            data = self.__dict__.copy()
            data.pop('id', None)
            new_id = self.__class__.create(**data)
            self.id = new_id

    @classmethod
    def update(cls, id: int, **kwargs) -> bool:
        """Update record with validation"""
        if not kwargs:
            raise ValueError("At least one field to update must be provided")
        
        # Validate fields
        validated_data = cls._validate_and_convert_values(**kwargs)
        
        conn = cls.connect()
        try:
            cursor = conn.cursor()
            set_clause = ', '.join([f"{k} = ?" for k in validated_data.keys()])
            values = list(validated_data.values())
            
            cursor.execute(
                f"UPDATE {cls.table_name} SET {set_clause} WHERE id = ?",
                (*values, id)
            )
            updated_rows = cursor.rowcount
            conn.commit()
            
            if updated_rows == 0:
                raise ValueError(f"No record found with id={id}")
            
            return True
        finally:
            conn.close()
        
    @classmethod
    def delete(cls, **filters) -> int:
        """Delete records"""
        if not filters:
            raise ValueError("At least one filter must be specified")
        
        valid_fields = cls._get_valid_fields()
        
        for key in filters.keys():
            if key not in valid_fields:
                raise ValueError(f"Invalid field name: {key}")
        
        conn = cls.connect()
        try:
            cursor = conn.cursor()
            where_clause = " AND ".join(f"{key} = ?" for key in filters.keys())
            values = tuple(filters.values())
            query = f"DELETE FROM {cls.table_name} WHERE {where_clause}"
            
            cursor.execute(query, values)
            deleted_count = cursor.rowcount
            conn.commit()
            return deleted_count
        finally:
            conn.close()


class SQLiteModel(BaseModel):
    """SQLite model class"""
    class Meta:
        db_config = {}
