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
    title = CharField(max_length=200, unique=True)
    class Meta:
        db_config = DATABASE_CONFIG['sqlite']
        table_name = 'categories'  # Name of the table for storing the Category model data in SQLite


class Post(SQLiteModel):
    title = CharField(max_length=100, unique=True)
    create_time = DateTimeField(auto_now=True)
    category = ForeignKey(Category)
    class Meta:
        db_config = DATABASE_CONFIG['sqlite'])
```
## Automatic Table Management
In the latest version of AbarORM, you no longer need to manually create tables. The library automatically handles the creation and management of your tables based on the model definitions. This means that as soon as you start interacting with your models, AbarORM will ensure that the corresponding tables are created if they do not already exist. However, you can manage the names of the tables manually by defining the `table_name` variable in the Meta class

## Automatic Schema Updates
AbarORM also supports automatic schema updates. If you add new fields to your models while the application is running, AbarORM will automatically update the database schema to reflect these changes. This eliminates the need for manual migration scripts or database rebuilds.

???+ warning
    While schema updates are handled automatically, it is advisable to recreate your database schema after completing development to ensure that all fields and constraints are correctly applied. This helps to avoid potential issues and ensures that your database is in a consistent state before moving to production.

## CRUD
There is no difference in the type and method of CRUD in modeling and using databases, and to create them, you can refer to a [Basic Usage - CRUD](/basic_usage/#step-3-perform-crud-operations) page.