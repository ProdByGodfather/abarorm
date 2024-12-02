# abarorm

| ![abarorm Logo](https://prodbygodfather.github.io/abarorm/images/logo.png) | **abarorm** is a lightweight and easy-to-use Object-Relational Mapping (ORM) library for SQLite, MySQL, and PostgreSQL databases in Python. It provides a simple and intuitive interface for managing database models and interactions. |
|----------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## Features

- Define models using Python classes.
- Automatically handle database schema creation and management.
- Support for basic CRUD (Create, Read, Update, Delete) operations.
- Manage foreign key relationships effortlessly.
- Custom field types with validation and constraints.
- **New in v1.0.0**: Automatic table creation and updates without needing explicit `create_table()` calls.
- **New in v2.0.0**: Added support for PostgreSQL databases.
- **New in v2.0.0**: Ordering by fields in the `all()` method.
- **New in v3.0.0**: Fixed table naming bugs to ensure consistent naming conventions.
- **New in v3.0.0**: Updated return values for methods to improve clarity and usability.
- **New in v3.0.0**: Enhanced `filter` method now supports `order_by` functionality for result ordering.
- **New in v3.2.0**: Added `__gte` and `__lte` functionality in the filter section.
- **New in v4.0.0**: Added `__repr__`, `count`, and `to_dict` methods for easier data manipulation and debugging.
- **New in v4.2.3**: Added `first()`, `last()`, `exists()`, and `paginate()` methods to the QuerySet class for more powerful querying capabilities.




## Installation

You can install [**abarorm**](https://pypi.org/project/abarorm/) from PyPI using pip:

```bash
pip install abarorm
```
For MySQL support, you also need to install `mysql-connector-python`:

```bash
pip install mysql-connector-python
```
For PostgreSQL support, you need to install `psycopg2-binary`:
```bash
pip install psycopg2-binary
```

## Documentation
For detailed documentation, examples, and advanced usage, please visit the [official abarorm documentation website](https://prodbygodfather.github.io/abarorm/).

## Database Configuration
Before defining models, you need to set up your database configuration. This involves specifying connection parameters for the database you are using (SQLite, MySQL, or PostgreSQL). Here’s an example of how to configure the database:
```python
# Database configuration
DATABASE_CONFIG = {
    'sqlite': {
        'db_name': 'example.db',  # Name of the SQLite database file
    },
    'mysql': {
        'host': 'localhost',
        'user': 'your_mysql_user',
        'password': 'your_mysql_password',
        'database': 'example_db',
    },
    'postgresql': {
        'host': 'localhost',
        'user': 'your_pg_user',
        'password': 'your_pg_password',
        'database': 'example_db',
    }
}
```
## Model Definition
After setting up the database configuration, you can define your models. A model is a representation of a database table. Here’s how to create a model using abarorm:
```python
from abarorm import SQLiteModel, MySQLModel, PostgreSQLModel
from abarorm.fields import CharField, DateTimeField, ForeignKey

# Define the Category model for SQLite
class Category(SQLiteModel):
    class Meta:
        db_config = DATABASE_CONFIG['sqlite']
        table_name = 'categories'  # Name of the table for storing the Category model data

    title = CharField(max_length=200, null=False)  # Title of the category, must be unique and not null
    create_time = DateTimeField(auto_now=True, auto_now_add=True)  # Automatically set to current datetime
    update_time = DateTimeField(auto_now=True)  # Automatically set to current datetime


# Define the Post model for MySQL
class Post(MySQLModel):
    class Meta:
        db_config = DATABASE_CONFIG['mysql']

    title = CharField(max_length=100, null=False)  # Title of the post, must be unique and not null
    create_time = DateTimeField(auto_now=True)  # Automatically set to current datetime
    category = ForeignKey(to=Category)  # Foreign key referring to the Category model
```
## CRUD Operations
Now that you have defined your models, you can perform CRUD operations. Here’s a breakdown of each operation:
### Create
To create new records in the database, use the `create()` method. For example:
```python
# Create a new category
Category.create(title='Movies')

# Create a new post
category = Category.get(id=1)  # Fetch the category with ID 1
if category:
    Post.create(title='Godfather', category=category.id)  # Create a new post associated with the fetched category
```
### Read
To read records from the database, use the `all()` or `get()` methods:
```python
# Retrieve all posts
all_posts = Post.all()

# Retrieve a specific post by ID
post_data = Post.get(id=1)
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

### Update
To update existing records, fetch the record, modify its attributes, and then save it:
```python
if post_data:
    post_data.title = "The Godfather"
    post_data.save()  # Save the updated post data
```
Or:
```python
Post.update(1, title='Updated Godfather')  # Update the title of the post with ID 1 to 'Updated Godfather'
```
### Delete
To delete a record from the database, use the `delete()` method:
```python
Post.delete(1)  # Delete the post with ID 1
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

## Version 4.2.3

- `first():` Added to return the first result in a `QuerySet`.
- `last():` Added to return the last result in a `QuerySet`.
- `exists():` Added to check if any records exist.
- `paginate():` Added to handle pagination for large result sets.


**Important for Developers:** When adding new fields to models, they will default to `NULL`. It’s recommended to recreate the database schema after development is complete to ensure fields have appropriate constraints and default values.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the [Apache-2.0 License](https://github.com/ProdByGodfather/abarorm/blob/main/LICENSE) - see the LICENSE file for details.

## Acknowledgements

- **Python**: The language used for this project.
- **SQLite & MySQL**: The databases supported by this project.
- **setuptools**: The tool used for packaging and distributing the library.
- **psycopg2-binary**: The PostgreSQL adapter used for connecting to PostgreSQL databases.