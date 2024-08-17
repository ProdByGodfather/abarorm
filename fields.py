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
    def __init__(self, auto_now: bool = False, **kwargs):
        super().__init__(field_type='DATETIME', **kwargs)
        self.auto_now = auto_now

class ForeignKey(Field):
    def __init__(self, to: Type['BaseModel'], on_delete: str = 'CASCADE', **kwargs):
        super().__init__(field_type='INTEGER', **kwargs)
        self.to = to
        self.on_delete = on_delete
