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
    },
    # This connection string model is used to connect to mysql and postgresql databases
    # which we have not used in this example
    'mysql': {
        'host': 'localhost',
        'user': 'your_mysql_user',
        'password': 'your_mysql_password',
        'database': 'example_db',
    },
}

# Define the Category model
class Category(SQLiteModel):
    title = CharField(max_length=200, unique=True)
    class Meta:
        db_config = DATABASE_CONFIG['sqlite']
        table_name = 'categories'  # Name of the table for storing the Category model data in SQLite


# Define the Post model
class Post(SQLiteModel):
    title = CharField(max_length=100, unique=True)
    create_time = DateTimeField(auto_now=True)
    category = ForeignKey(Category)
    class Meta:
        db_config = DATABASE_CONFIG['sqlite']
```
In the example above:

**Category** and Post are two models representing database tables.
Each class inherits from `SQLiteModel` and defines fields using AbarORM’s built-in field types.

## Step 2: Perform CRUD Operations
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
all_posts = Post.all(order_by='-create_time')
print("All posts:", all_posts)
# Retrieve a specific post
post_data = Post.get(id=1)
if post_data:
    print("Post with ID 1:", post_data)
```
### Filtering Records
The `filter()` method allows you to retrieve records based on specified criteria. You can use keyword arguments to filter by field values and sort the results using `order_by`.
```python
# Filter posts by category ID and order by creation time
filtered_posts = Post.filter(category=category.id, order_by='-create_time')
```
#### Advanced Filtering
You can also use special lookup expressions like `__gte` (greater than or equal to) and `__lte` (less than or equal to) for more complex queries:
```python
# Retrieve posts created after a specific date
filtered_posts = Post.filter(create_time__gte='2024-01-01 00:00:00')
```

### Update Records
To update existing records, use the `update` method:
```python
# Update a post
Post.update(id=1, title='The Godfather Part II')
```
However, you can update a field at the same time when you receive it:
```python
category = Category.get(id=id)
category.title = title
category.save()
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