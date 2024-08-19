# Introduction to AbarORM


## What is AbarORM?
**AbarORM** is a lightweight and easy-to-use Object-Relational Mapping (ORM) library designed for SQLite databases in Python. It provides a simple and intuitive interface for managing database models and interactions, making it easier for developers to work with databases without needing to write raw SQL queries.

## Key Features

- **Simplicity**: AbarORM is designed to be straightforward and easy to use. With a clean API, you can define your database models and interact with your database using Python objects.
- **Automatic Schema Management**: The library handles the creation and management of the database schema automatically, so you don't have to worry about writing migration scripts.
- **CRUD Operations**: It supports all basic CRUD (Create, Read, Update, Delete) operations, allowing you to perform database operations with minimal code.
- **Relationships**: AbarORM supports foreign key relationships between models, making it easier to manage complex data structures.
- **Custom Fields**: You can define custom field types with validation and constraints to suit your specific needs.


## Why Choose AbarORM?

### Django ORM-Like Experience

If you're familiar with **Django ORM**, you'll find AbarORM's approach to database modeling and interactions quite familiar. AbarORM follows many of the same principles and patterns found in Django ORM, such as:

- **Model Definition**: Just like in Django ORM, you define your database tables using Python classes. Each class represents a table, and class attributes define the columns of the table.
- **Field Types**: AbarORM uses similar field types to Django ORM (e.g., `CharField`, `DateTimeField`, `ForeignKey`), making it easy for Django users to adapt to AbarORM.
- **Automatic Schema Management**: Similar to Django's migrations, AbarORM handles schema creation and updates automatically based on your model definitions.


## Ease of Use

AbarORM aims to reduce the complexity associated with database interactions. By abstracting away the details of SQL queries and database management, it allows developers to focus more on writing application logic rather than dealing with database intricacies.

## Flexibility

While it is lightweight, AbarORM is flexible enough to handle various use cases. Whether you're working on a small personal project or a more complex application, AbarORM can adapt to your needs.

## Pythonic Approach

The library follows Pythonic principles, offering a seamless integration with Python's data structures and object-oriented features. This approach ensures that working with your database feels natural and intuitive.

## Getting Started

To get started with AbarORM, follow these steps:

1. **Installation**: Install the library via pip:
   ```bash
   pip install abarorm
   ```
**Setup:** Configure your database connection and define your models by inheriting from `SQLiteModel` or `MySQLModel` depending on your database type.

**Define Models:** Create Python classes that represent your database tables. Use built-in field types to define the attributes of each model.

**Create Tables:** Use the create_table method to initialize your database schema.

**Perform Operations:** Use the methods provided by AbarORM to perform CRUD operations, manage relationships, and query your data.

For detailed instructions and examples, refer to the [Basic Usage](basic_usage.md) section of the documentation.

# Example
Here's a quick example of defining a simple model with AbarORM on SQLite:
```python
from abarorm import SQLiteModel
from abarorm.fields import CharField, DateTimeField

DATABASE_CONFIG = {
    'sqlite': {
        'db_name': 'example.db',
    }
}

class Category(SQLiteModel):
    table_name = 'categories'
    title = CharField(max_length=200, unique=True)

    def __init__(self, **kwargs):
        super().__init__(db_config=DATABASE_CONFIG['sqlite'], **kwargs)

# Create the table in the database
Category.create_table()

# Add a new category
Category.create(title='Movies')
```