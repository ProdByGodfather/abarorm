from typing import Type, Optional

class Field:
    def __init__(self, field_type: str, max_length: Optional[int] = None, min_length: Optional[int] = None,
                 unique: bool = False, null: bool = False, default: Optional[str] = None):
        self.field_type = field_type
        self.max_length = max_length
        self.min_length = min_length
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
        super().__init__(field_type='BOOLEAN', default=default, **kwargs)

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
    def __init__(self, to: Type['BaseModel'], on_delete: str = 'CASCADE', **kwargs):
        super().__init__(field_type='INTEGER', **kwargs)
        self.to = to  # This is the related model class
        self.on_delete = on_delete  # Specifies the behavior when the referenced row is deleted
        
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
    def __init__(self, **kwargs):
        super().__init__(max_length=254, **kwargs)

class URLField(CharField):
    def __init__(self, **kwargs):
        super().__init__(max_length=1000, **kwargs)
