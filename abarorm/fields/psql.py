from typing import Type, Optional
import re
import datetime


class Field:
    """Base field class for all PostgreSQL field types"""
    
    def __init__(self, field_type: str, max_length: Optional[int] = None, unique: bool = False,
                 null: bool = False, default: Optional[str] = None):
        self.field_type = field_type
        self.max_length = max_length
        self.unique = unique
        self.null = null
        self.default = default
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(type={self.field_type}, null={self.null}, unique={self.unique})>"
    
    def validate(self, value):
        """Base validation - override in subclasses"""
        if value is None and not self.null:
            raise ValueError(f"{self.__class__.__name__} cannot be null")
        return value


class CharField(Field):
    """Character field with max_length validation"""
    
    def __init__(self, max_length: int = 255, **kwargs):
        super().__init__(field_type='VARCHAR', max_length=max_length, **kwargs)
    
    def validate(self, value):
        if value is None:
            if not self.null:
                raise ValueError("CharField cannot be null")
            return None
        
        if not isinstance(value, str):
            value = str(value)
        
        if self.max_length and len(value) > self.max_length:
            raise ValueError(
                f"Value length ({len(value)}) exceeds max_length ({self.max_length})"
            )
        
        return value


class IntegerField(Field):
    """Integer field with type validation"""
    
    def __init__(self, **kwargs):
        super().__init__(field_type='INTEGER', **kwargs)
    
    def validate(self, value):
        if value is None:
            if not self.null:
                raise ValueError("IntegerField cannot be null")
            return None
        
        try:
            return int(value)
        except (ValueError, TypeError):
            raise ValueError(f"Cannot convert '{value}' to integer")


class BooleanField(Field):
    """Boolean field stored as BOOLEAN in PostgreSQL"""
    
    def __init__(self, default: bool = False, **kwargs):
        super().__init__(field_type='BOOLEAN', default=default, **kwargs)
        self.default_bool = default
    
    def set_default(self):
        """Return PostgreSQL default value"""
        return 'TRUE' if self.default else 'FALSE'
    
    def validate(self, value):
        if value is None:
            if not self.null:
                raise ValueError("BooleanField cannot be null")
            return None
        
        # PostgreSQL accepts boolean directly
        if isinstance(value, bool):
            return value
        
        # Convert string to boolean
        if isinstance(value, str):
            if value.lower() in ('true', '1', 't', 'yes', 'y'):
                return True
            elif value.lower() in ('false', '0', 'f', 'no', 'n'):
                return False
            else:
                raise ValueError(f"Cannot convert '{value}' to boolean")
        
        # Convert int to boolean
        return bool(value)
    
    def to_python(self, value):
        """Convert database value to Python bool"""
        if value is None:
            return None
        return bool(value)


class DateTimeField(Field):
    """DateTime field with auto_now and auto_now_add support"""
    
    def __init__(self, auto_now: bool = False, auto_now_add: Optional[bool] = None, **kwargs):
        super().__init__(field_type='TIMESTAMP', **kwargs)
        self.auto_now = auto_now
        self.auto_now_add = auto_now_add
    
    def validate(self, value):
        if value is None:
            if not self.null:
                raise ValueError("DateTimeField cannot be null")
            return None
        
        # If already a datetime object
        if isinstance(value, datetime.datetime):
            return value
        
        # If string, try to parse
        if isinstance(value, str):
            try:
                return datetime.datetime.fromisoformat(value)
            except ValueError:
                try:
                    return datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    raise ValueError(f"Invalid datetime format: {value}")
        
        raise ValueError(f"Invalid type for DateTimeField: {type(value).__name__}")
    
    def to_python(self, value):
        """Convert database value to Python datetime"""
        if value is None:
            return None
        if isinstance(value, datetime.datetime):
            return value
        return datetime.datetime.fromisoformat(str(value))


class DateField(Field):
    """Date field with auto_now and auto_now_add support"""
    
    def __init__(self, auto_now: bool = False, auto_now_add: Optional[bool] = None, **kwargs):
        super().__init__(field_type='DATE', **kwargs)
        self.auto_now = auto_now
        self.auto_now_add = auto_now_add
    
    def validate(self, value):
        if value is None:
            if not self.null:
                raise ValueError("DateField cannot be null")
            return None
        
        if isinstance(value, datetime.date):
            return value
        
        if isinstance(value, str):
            try:
                return datetime.date.fromisoformat(value)
            except ValueError:
                raise ValueError(f"Invalid date format: {value}. Expected ISO format (YYYY-MM-DD).")
        
        raise ValueError(f"Invalid type for DateField: {type(value).__name__}")
    
    def to_python(self, value):
        """Convert database value to Python date"""
        if value is None:
            return None
        if isinstance(value, datetime.date):
            return value
        return datetime.date.fromisoformat(str(value))


class TimeField(Field):
    """Time field"""
    
    def __init__(self, **kwargs):
        super().__init__(field_type='TIME', **kwargs)
    
    def validate(self, value):
        if value is None:
            if not self.null:
                raise ValueError("TimeField cannot be null")
            return None
        
        if isinstance(value, datetime.time):
            return value
        
        if isinstance(value, str):
            try:
                return datetime.time.fromisoformat(value)
            except ValueError:
                raise ValueError(f"Invalid time format: {value}. Expected ISO format (HH:MM:SS).")
        
        raise ValueError(f"Invalid type for TimeField: {type(value).__name__}")
    
    def to_python(self, value):
        """Convert database value to Python time"""
        if value is None:
            return None
        if isinstance(value, datetime.time):
            return value
        return datetime.time.fromisoformat(str(value))


class ForeignKey(Field):
    """Foreign key field with relationship support"""
    
    def __init__(self, to: Type['BaseModel'], on_delete: str = 'CASCADE',
                 related_name: Optional[str] = None, **kwargs):
        super().__init__(field_type='INTEGER', **kwargs)
        self.to = to
        self.on_delete = on_delete.upper()
        self.related_name = related_name
        
        # Validate on_delete option
        valid_options = ['CASCADE', 'SET NULL', 'RESTRICT', 'NO ACTION', 'SET DEFAULT']
        if self.on_delete not in valid_options:
            raise ValueError(
                f"Invalid on_delete option: {on_delete}. "
                f"Valid options: {', '.join(valid_options)}"
            )
    
    def validate(self, value):
        """Validate foreign key value"""
        if value is None:
            if not self.null:
                raise ValueError("ForeignKey cannot be null")
            return None
        
        # Accept either ID (int) or model instance
        if isinstance(value, int):
            return value
        
        if isinstance(value, self.to):
            if not hasattr(value, 'id') or value.id is None:
                raise ValueError(f"Related {self.to.__name__} instance must have an ID")
            return value.id
        
        raise ValueError(
            f"ForeignKey must be an integer ID or instance of {self.to.__name__}, "
            f"got {type(value).__name__}"
        )
    
    def get_constraint(self, field_name: str, table_name: str) -> str:
        """Generate SQL FOREIGN KEY constraint for PostgreSQL"""
        return (
            f"ALTER TABLE {table_name} "
            f"ADD CONSTRAINT fk_{table_name}_{field_name} "
            f"FOREIGN KEY ({field_name}) "
            f"REFERENCES {self.to.table_name}(id) "
            f"ON DELETE {self.on_delete}"
        )


class FloatField(Field):
    """Float field stored as REAL in PostgreSQL"""
    
    def __init__(self, **kwargs):
        super().__init__(field_type='REAL', **kwargs)
    
    def validate(self, value):
        if value is None:
            if not self.null:
                raise ValueError("FloatField cannot be null")
            return None
        
        try:
            return float(value)
        except (ValueError, TypeError):
            raise ValueError(f"Cannot convert '{value}' to float")


class DecimalField(Field):
    """Decimal field with precision validation"""
    
    def __init__(self, max_digits: int, decimal_places: int, **kwargs):
        super().__init__(field_type='DECIMAL', **kwargs)
        self.max_digits = max_digits
        self.decimal_places = decimal_places
        
        if decimal_places > max_digits:
            raise ValueError("decimal_places cannot be greater than max_digits")
    
    def validate(self, value):
        if value is None:
            if not self.null:
                raise ValueError("DecimalField cannot be null")
            return None
        
        try:
            value = float(value)
        except (ValueError, TypeError):
            raise ValueError(f"Cannot convert '{value}' to decimal")
        
        # Check total digits (excluding decimal point and sign)
        value_str = str(abs(value)).replace('.', '')
        if len(value_str) > self.max_digits:
            raise ValueError(
                f"Value {value} has {len(value_str)} digits, "
                f"exceeds max_digits={self.max_digits}"
            )
        
        # Check decimal places
        decimal_part = str(value).split('.')[-1] if '.' in str(value) else ''
        if len(decimal_part) > self.decimal_places:
            raise ValueError(
                f"Value {value} has {len(decimal_part)} decimal places, "
                f"exceeds decimal_places={self.decimal_places}"
            )
        
        return value


class TextField(Field):
    """Large text field without length limit"""
    
    def __init__(self, **kwargs):
        super().__init__(field_type='TEXT', **kwargs)
    
    def validate(self, value):
        if value is None:
            if not self.null:
                raise ValueError("TextField cannot be null")
            return None
        
        if not isinstance(value, str):
            value = str(value)
        
        return value


class EmailField(CharField):
    """Email field with validation"""
    
    EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    def __init__(self, max_length: int = 255, **kwargs):
        super().__init__(max_length=max_length, **kwargs)
    
    def validate(self, value):
        if value is None:
            if not self.null:
                raise ValueError("EmailField cannot be null")
            return None
        
        # First apply CharField validation (type and length)
        value = super().validate(value)
        
        # Then validate email format
        if not re.match(self.EMAIL_REGEX, value):
            raise ValueError(f"Invalid email address: '{value}'")
        
        return value


class URLField(CharField):
    """URL field with validation"""
    
    URL_REGEX = r'^(https?|ftp)://[^\s/$.?#].[^\s]*$'
    
    def __init__(self, max_length: int = 2048, **kwargs):
        super().__init__(max_length=max_length, **kwargs)
    
    def validate(self, value):
        if value is None:
            if not self.null:
                raise ValueError("URLField cannot be null")
            return None
        
        # First apply CharField validation
        value = super().validate(value)
        
        # Then validate URL format
        if not re.match(self.URL_REGEX, value, re.IGNORECASE):
            raise ValueError(f"Invalid URL: '{value}'")
        
        return value
