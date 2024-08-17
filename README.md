# abarorm

**abarorm** is a lightweight and easy-to-use Object-Relational Mapping (ORM) library for SQLite databases in Python. It aims to provide a simple and intuitive interface for managing database models and interactions.

## Features

- Define models using Python classes
- Automatically handle database schema creation and management
- Support for basic CRUD operations
- Foreign key relationships
- Custom field types with validation and constraints

## Installation

You can install **abarorm** from PyPI using pip:

```bash
pip install abarorm
```

## Basic Usage
Here’s a quick overview of how to use **abarorm** to define models and interact with an SQLite database.

## Defining Models
Create a new Python file (e.g., `models.py`) and define your models by inheriting from `SQLiteModel`:

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
        # Initialize the Category model with database configuration
        super().__init__(db_config=DATABASE_CONFIG['sqlite'], **kwargs)
        
class Post(SQLiteModel):
    table_name = 'posts'
    title = CharField(max_length=100, unique=True)
    create_time = DateTimeField(auto_now=True)
    category = ForeignKey(Category)
    def __init__(self, **kwargs):
        # Initialize the Category model with database configuration
        super().__init__(db_config=DATABASE_CONFIG['sqlite'], **kwargs)
```

## Creating Tables
Create the tables in the database by calling the `create_table` method on your model classes:

```python
if __name__ == "__main__":
    Category.create_table()
    Post.create_table()
```
## Adding Data
You can add new records to the database using the `create` method:
```python
# Adding a new category
Category.create(title='Movies')

# Adding a new post
category = Category.get(id=1)  # Fetch the category with ID 1
if category:
    Post.create(title='Godfather', category=category.id)
```
## Querying Data
Retrieve all records or filter records based on criteria:

```python
# Retrieve all posts
all_posts = Post.all()
print("All Posts:", [(post.title, post.category) for post in all_posts])

# Retrieve a specific post
post_data = Post.get(id=1)
if post_data:
    print("Post with ID 1:", post_data.title, post_data.category)

# Filter posts by category
filtered_posts = Post.filter(category=category.id)
print("Filtered Posts:", [(post.title, post.category) for post in filtered_posts])
```
## Updating Records
Update existing records with the `update` method:
```python
Update existing records with the update method:
```
## Deleting Records
Delete records using the `delete` method:
```python
Post.delete(1)
```

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on [github](github.com/prodbygodfather/abarorm).

## License
This project is licensed under the MIT License - see the [License](github.com/prodbygodfather/abarorm/License) file for details.

## Acknowledgements

- **Python**: The language used for this project
- **SQLite**: The database used for this project
- **setuptools**: The tool used for packaging and distributing the library