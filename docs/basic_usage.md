---
title: "Basic Usage of AbarORM"
---

# Basic Usage of AbarORM

## Overview

In this section, we will cover the basic usage of AbarORM, including how to define models, create tables, and perform basic CRUD operations. This guide assumes you have already installed AbarORM and are familiar with Python.

## Step 1: Define Your Models

To start using AbarORM, you first need to define your database models. Each model corresponds to a table in your database. Here’s how you can define a simple model:

### Example: Defining Models

```python
from abarorm import SQLiteModel
from abarorm.fields.sqlite import CharField, DateTimeField, ForeignKey
from abarorm.fields import psql

# Database configuration
DATABASE_CONFIG = {
    'sqlite': {
        'db_name': 'example.db',  # Name of the SQLite database file
    },
    # This connection string model is used to connect to postgresql database
    # which we have not used in this example
    'postgresql': {
        'host': 'localhost',
        'user': 'hoopad',
        'password': 'db_password',
        'database': 'example_db',  
        'port': 5432,
    }
}

# Define the Category model
class Category(SQLiteModel):
    title = CharField(max_length=200, unique=True)
    class Meta:
        db_config = DATABASE_CONFIG['sqlite']
        table_name = 'categories'  # Name of the table for storing the Category model data in SQLite


# Define the Post model
class Post(SQLiteModel):
    title = psql.CharField(max_length=100, unique=True)
    create_time = psql.DateTimeField(auto_now=True)
    category = psql.ForeignKey(Category)
    class Meta:
        db_config = DATABASE_CONFIG['postgresql']
```

!!! info inline end "Note"

    The fields in PostgreSQL and SQLite databases are structurally the same and are designed to be used in the same way, but to use either database, you must use fields from the same database in your models. For example, the path to `sqlite` fields is: `abarorm.fields.sqlite` and the path to `postgresql` fields is: `abarorm.fields.psql`

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

### Converting to Dictionary and Counting Records
After performing operations on the model, you can convert records to dictionaries using the `to_dict()` method and count the number of records using the `count()` method.

#### `to_dict` Method
The `to_dict()` method converts a model instance into a dictionary, making it easier to manipulate and serialize the data.

**Example:**
```python
# Retrieve a post by ID
post = Post.get(id=1)

# Convert the post to a dictionary
post_dict = post.all().to_dict()
print(post_dict)
# Output: [{'id': 1, 'title': 'Godfather', 'create_time': '2024-01-01 12:00:00', ...}]
```

#### `count` Method
The `count()` method allows you to get the number of records in a model's table.

**Example:**
```python
# Count the number of posts in the database
num_posts = Post.count()
print(num_posts)  # Output: 10 (if there are 10 posts in the database)
```


#### `first()`, `last()`, `exists()`, `order_by()`, and `paginate()`
- `first():` Returns the first result or None if no results are present.
- `last():` Returns the last result or None if no results are present.
- `exists():` Checks if any records exist in the `QuerySet`.
- `paginate():` Handles pagination of results, allowing you to retrieve subsets of data based on page and page size.

**Example:**
```python
# Check if any posts exist
exists = Post.all().exists()

# Get the first post
first_post = Post.all().first()

# Get the last post
last_post = Post.all().last()

# Paginate the results
paginated_posts = Post.all().paginate(1, 5)  # Page 1, 5 results per page

# Using multiple querysets in one query
posts = Post.filter(title='Godfather').order_by('create_time').paginate(1, 4).to_dict()
```

These methods are particularly useful for data manipulation and debugging, as they provide a simple way to view and interact with your database records.


## Summary

This guide covered the basic usage of AbarORM, including model definition, table creation, and CRUD operations. For more advanced features and configurations, refer to the [Field Types](/abarorm/field_types.md) section.