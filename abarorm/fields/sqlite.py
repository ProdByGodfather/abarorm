from typing import Type, Optional
import re

class Field:
    def __init__(self, field_type: str, max_length: Optional[int] = None, unique: bool = False,
                 null: bool = False, default: Optional[str] = None):
        self.field_type = field_type
        self.max_length = max_length
        self.unique = unique
        self.null = null
        self.default = default

class CharField(Field):
    def __init__(self, max_length: int = 255, **kwargs):
        super().__init__(field_type='TEXT', max_length=max_length, **kwargs)

class IntegerField(Field):
    def __init__(self, **kwargs):
        super().__init__(field_type='INTEGER', **kwargs)

class BooleanField(Field):
    def __init__(self, default: bool = False, **kwargs):
        super().__init__(field_type='BOOLEAN', default=str(int(default)), **kwargs)  # Convert bool to int


class DateTimeField(Field):
    def __init__(self, auto_now: bool = False, auto_now_add: Optional[bool] = None, **kwargs):
        super().__init__(field_type='DATETIME', **kwargs)
        self.auto_now = auto_now
        self.auto_now_add = auto_now_add

class DateField(Field):
    def __init__(self, auto_now: bool = False, auto_now_add: Optional[bool] = None, **kwargs):
        super().__init__(field_type='DATE', **kwargs)
        self.auto_now = auto_now
        self.auto_now_add = auto_now_add

class TimeField(Field):
    def __init__(self, **kwargs):
        super().__init__(field_type='TIME', **kwargs)

class ForeignKey(Field):
    def __init__(self, to: Type['BaseModel'], on_delete: str = 'CASCADE',
                 related_name: Optional[str] = None, **kwargs):
        super().__init__(field_type='INTEGER', **kwargs)
        self.to = to  
        self.on_delete = on_delete 
        self.related_name = related_name  

class FloatField(Field):
    def __init__(self, **kwargs):
        super().__init__(field_type='FLOAT', **kwargs)

class DecimalField(Field):
    def __init__(self, max_digits: int, decimal_places: int, **kwargs):
        super().__init__(field_type='DECIMAL', **kwargs)
        self.max_digits = max_digits
        self.decimal_places = decimal_places

class TextField(Field):
    def __init__(self, **kwargs):
        super().__init__(field_type='TEXT', **kwargs)

class EmailField(CharField):
    EMAIL_REGEX = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    
    def __init__(self, max_length: int = 255, **kwargs):
        super().__init__(max_length=max_length, **kwargs)
    
    def validate(self, value: str):
        if not re.match(self.EMAIL_REGEX, value):
            raise ValueError(f"Invalid email address: {value}")

class URLField(CharField):
    URL_REGEX = r'^(https?|ftp)://[^\s/$.?#].[^\s]*$'
    
    def __init__(self, max_length: int = 2048, **kwargs):
        super().__init__(max_length=max_length, **kwargs)
    
    def validate(self, value: str):
        if not re.match(self.URL_REGEX, value):
            raise ValueError(f"Invalid URL: {value}")
