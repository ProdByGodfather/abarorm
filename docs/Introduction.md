# Introduction to AbarORM


## What is AbarORM?
**AbarORM** is a lightweight and easy-to-use Object-Relational Mapping (ORM) library designed for SQLite and PostgreSQL databases in Python. It provides a simple and intuitive interface for managing database models and interactions, making it easier for developers to work with databases without needing to write raw SQL queries.
## Key Features


- **Simplicity:** AbarORM is designed to be straightforward and easy to use. With a clean API, you can define your database models and interact with your database using Python objects.
- **Automatic Schema Management:** The library handles the creation and management of the database schema automatically, so you don't have to worry about writing migration scripts. Tables are created or updated based on your model definitions.
- **CRUD Operations:** It supports all basic CRUD (Create, Read, Update, Delete) operations, allowing you to perform database operations with minimal code.
- **Order By Support:** AbarORM includes support for ordering query results, providing more flexibility in retrieving data.
- **Foreign Key Relationships:** AbarORM supports foreign key relationships between models, making it easier to manage complex data structures.
- **Custom Fields:** You can define custom field types with validation and constraints to suit your specific needs.
- **PostgreSQL Support:** In addition to SQLite, AbarORM now supports PostgreSQL, providing a broader range of database options.

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

**Installation**: 
To get started with AbarORM, follow these steps:

Install the library via pip:
```bash
pip install abarorm
```
For MySQL support, you also need to install `mysql-connector-python`: (Required)
```bash
pip install mysql-connector-python
```
For PostgreSQL support, install `psycopg2-binary`: (Required)
```bash
pip install psycopg2-binary
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
    title = CharField(max_length=200, unique=True)
    create_time = DateTimeField(auto_now_add=True)
    update_time = DateTimeField(auto_now=True)
    
    class Meta:
        db_config = DATABASE_CONFIG['sqlite']

# Add a new category
Category.create(title='Movies')

```
The configuration of each database is different, but the simplest available configuration is for sqlite, which can be connected to it simply with a database name.

Models are automatically managed by AbarORM, which means that any changes to your models, such as adding new fields, are automatically applied to the database without the need for manual migration steps. This feature streamlines development by reducing the overhead associated with schema changes.

???+ warning 
    While this automatic management is convenient during development, it's advisable to recreate your database after completing development. This ensures that all schema changes are properly applied and that the database structure is optimized for production.