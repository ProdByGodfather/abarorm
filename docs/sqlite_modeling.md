# SQLite Model Modeling

In this section, we cover how to define models for SQLite using the AbarORM library.

## Basic Example

To use SQLite with AbarORM, you need to define your models by inheriting from `SQLiteModel`. Here is a basic example:

```python
from abarorm import SQLiteModel
from abarorm.fields import CharField, DateTimeField, ForeignKey

DATABASE_CONFIG = {
    'sqlite': {
        'db_name': 'example.db',  # Name of the SQLite database file
    }
}

class Category(SQLiteModel):
    table_name = 'categories'
    title = CharField(max_length=200, unique=True)

    def __init__(self, **kwargs):
        super().__init__(db_config=DATABASE_CONFIG['sqlite'], **kwargs)

class Post(SQLiteModel):
    table_name = 'posts'
    title = CharField(max_length=100, unique=True)
    create_time = DateTimeField(auto_now=True)
    category = ForeignKey(Category)

    def __init__(self, **kwargs):
        super().__init__(db_config=DATABASE_CONFIG['sqlite'], **kwargs)
```
## Creating Tables

To create the tables in the SQLite database, call the `create_table` method on your model classes:
```python
if __name__ == "__main__":
    Category.create_table()
    Post.create_table()
```
## CRUD
There is no difference in the type and method of CRUD in modeling and using databases, and to create them, you can refer to a [Basic Usage - CRUD](http://127.0.0.1:8000/basic_usage/#step-3-perform-crud-operations) page.