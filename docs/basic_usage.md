# Basic Usage of AbarORM

## Overview

In this section, we will cover the basic usage of AbarORM, including how to define models, create tables, and perform basic CRUD operations. This guide assumes you have already installed AbarORM and are familiar with Python.

## Step 1: Define Your Models

To start using AbarORM, you first need to define your database models. Each model corresponds to a table in your database. Here’s how you can define a simple model:

### Example: Defining Models

```python
from abarorm import SQLiteModel
from abarorm.fields import CharField, DateTimeField, ForeignKey

# Database configuration
DATABASE_CONFIG = {
    'sqlite': {
        'db_name': 'example.db',  # Name of the SQLite database file
    }
}

# Define the Category model
class Category(SQLiteModel):
    table_name = 'categories'
    title = CharField(max_length=200, unique=True)

    def __init__(self, **kwargs):
        super().__init__(db_config=DATABASE_CONFIG['sqlite'], **kwargs)

# Define the Post model
class Post(SQLiteModel):
    table_name = 'posts'
    title = CharField(max_length=100, unique=True)
    create_time = DateTimeField(auto_now=True)
    category = ForeignKey(Category)

    def __init__(self, **kwargs):
        super().__init__(db_config=DATABASE_CONFIG['sqlite'], **kwargs)
```
In the example above:

**Category** and Post are two models representing database tables.
Each class inherits from `SQLiteModel` and defines fields using AbarORM’s built-in field types.

## Step 2: Create Tables
After defining your models, you need to create the corresponding tables in the database. Use the create_table method provided by AbarORM.
```python
# Create tables in the database
if __name__ == "__main__":
    Category.create_table()
    Post.create_table()
```
This script will create the tables `categories` and `posts` in the example.db `SQLite` database file.

## Step 3: Perform CRUD Operations
Once your tables are created, you can perform CRUD (Create, Read, Update, Delete) operations on your models.

### Create Records
To add new records to the database, use the `create` method:
```python
# Add a new category
Category.create(title='Movies')

# Add a new post
category = Category.get(id=1)  # Fetch the category with ID 1
if category:
    Post.create(title='Godfather', category=category.id)
```
### Read Records
To retrieve records from the database, use the `all`, `get`, or `filter` methods:
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
### Update Records
To update existing records, use the `update` method:
```python
# Update a post
Post.update(id=1, title='The Godfather Part II')
```
### Delete Records
To delete records, use the `delete` method:
```python
# Delete a post
Post.delete(1)
```
### Handling Relationships
Handling Relationships
AbarORM supports foreign key relationships between models. In the example provided, the `Post` model has a foreign key relationship with the `Category` model. This allows you to create complex data structures and manage related data efficiently.

### Example: Accessing Related Data
```python
# Access the category of a post
post = Post.get(id=1)
if post:
    category = Category.get(id=post.category)
    print("Post Category:", category.title)
```

## Summary

This guide covered the basic usage of AbarORM, including model definition, table creation, and CRUD operations. For more advanced features and configurations, refer to the [Field Types](field_types.md) section.