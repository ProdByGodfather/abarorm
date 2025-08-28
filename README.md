# abarorm

| ![abarorm Logo](https://prodbygodfather.github.io/abarorm/images/logo.png) | **abarorm** is a lightweight and easy-to-use Object-Relational Mapping (ORM) library for SQLite and PostgreSQL databases in Python. It provides a simple and intuitive interface for managing database models and interactions. |
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
- **New in v4.0.0**: Added `__repr__`, `count`, and `to_dict` methods.
- **New in v4.2.3**: Added `first()`, `last()`, `exists()`, and `paginate()` methods to the QuerySet class.
- **New in v5.0.0**: Fix `PostgreSQL` Bugs and structure.
- **New in v5.1.0**: Enhanced functionality for better usability for `delete` and `contains` methods.
- **New in v5.2.0**: Introduced `bulk_create` for efficient batch insertions.
- **New in v5.3.0**: Added `filter` support to the QuerySet class for in-memory filtering.
- **New in v5.4.0**: PostgreSQL database creation improved, added `related_name` support for ForeignKeys.




## Installation

You can install [**abarorm**](https://pypi.org/project/abarorm/) from PyPI using pip:

```bash
pip install abarorm
```

For PostgreSQL support, you need to install `psycopg2-binary`:
```bash
pip install psycopg2-binary
```

## Documentation
For detailed documentation, examples, and advanced usage, please visit the [official abarorm documentation website](https://prodbygodfather.github.io/abarorm/).

## Database Configuration
Before defining models, you need to set up your database configuration. This involves specifying connection parameters for the database you are using (SQLite and PostgreSQL). Here’s an example of how to configure the database:
```python
# Database configuration
DATABASE_CONFIG = {
    'sqlite': {
        'db_name': 'example.db',  # Name of the SQLite database file
    },
    'postgresql': {
        'host': 'localhost',
        'user': 'hoopad',
        'password': 'db_password',
        'database': 'example_db',  # Ensure this matches everywhere
        'port': 5432,
    }
}
```
## Model Definition
After setting up the database configuration, you can define your models. A model is a representation of a database table. Here’s how to create a model using abarorm:
```python
from abarorm import SQLiteModel, PostgreSQLModel
from abarorm.fields.sqlite import CharField, DateTimeField, ForeignKey
from abarorm.fields import psql

# Define the Category model for SQLite
class Category(SQLiteModel):
    class Meta:
        db_config = DATABASE_CONFIG['sqlite']
        table_name = 'categories'  # Name of the table for storing the Category model data

    title = CharField(max_length=200, null=False)  # Title of the category, must be unique and not null
    create_time = DateTimeField(auto_now=True, auto_now_add=True)  # Automatically set to current datetime
    update_time = DateTimeField(auto_now=True)  # Automatically set to current datetime


# Define the Post model for Postgresql
class Post(PostgreSQLModel):
    class Meta:
        db_config = DATABASE_CONFIG['postgresql']

    title = psql.CharField(max_length=100, null=False)  # Title of the post, must be unique and not null
    create_time = psql.DateTimeField(auto_now=True)  # Automatically set to current datetime
    category = psql.ForeignKey(to=Category, related_name='posts')  # Foreign key referring to the Category model
```
## CRUD Operations
Now that you have defined your models, you can perform CRUD operations. Here’s a breakdown of each operation:
### Create
To create new records in the database, use the `create()` method or **Bulk Create**: `bulk_create`. For example:
```python
# Create a new category
Category.create(title='Movies')

# Create a new post
category = Category.get(id=1)  # Fetch the category with ID 1
if category:
    Post.create(title='Godfather', category=category.id)  # Create a new post associated with the fetched category

# Bulk Create Post
records = [
    {"title": "Godfather Part II", "category": 1},
    {"title": "Godfather Part III", "category": 1},
]
Post.bulk_create(records)
```
### Read
To read records from the database, use the `all()` or `get()` methods:
```python
# Retrieve all posts
all_posts = Post.all()

# Retrieve a specific post by ID
post_data = Post.get(id=1)

# Related records via related_name
cat = Category.get(id=1)
cat_posts = cat.posts.all()  # Returns a fully functional QuerySet
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
Post.delete(id=1)  # Delete the post with ID 1
# or Removal based on a sometimes repeated argument
Post.delete(title='Godfather')
```
## Converting to Dictionary, Counting Records, and Other Query Methods

This section covers how to convert records to dictionaries, count records, and use various query methods like `first()`, `last()`, `exists()`, `order_by()`, `paginate()`, and `contains()`. These methods are essential for data manipulation, debugging, and optimizing query performance.

### `to_dict()` Method
The `to_dict()` method converts a model instance (or a collection of instances) into a dictionary, which is particularly useful for data manipulation and serialization. It makes it easier to work with the data in Python or send it over an API.

#### Example:
```python
# Retrieve all posts
posts = Post.all()

# Convert the collection of posts to a list of dictionaries
posts_dict = posts.to_dict()
print(posts_dict)
# Output: [{'id': 1, 'title': 'Godfather', 'create_time': '2024-01-01 12:00:00', ...}, {...}]
```

#### `count` Method
The `count()` method returns the number of records that match the query. It’s an efficient way to find the size of a dataset without retrieving the actual data.

**Example:**
```python
# Count the number of posts in the database
num_posts = Post.count()
print(num_posts)  # Output: 10 (if there are 10 posts in the database)
```

The `count()` method can also be used after applying filters to count specific records:
```python
# Count the number of posts with a specific title
num_posts_with_title = Post.filter(title='Godfather').count()
print(num_posts_with_title)  # Output: 3 (if there are 3 posts with the title 'Godfather')
```



#### `first()`, `last()`, `exists()`, `order_by()`, `paginate()` and `contains()`
- **`first()`**: Returns the first result or `None` if no results are present.
- **`last()`**: Returns the last result or `None` if no results are present.
- **`exists()`**: Checks if any records exist in the `QuerySet`.
- **`paginate()`**: Handles pagination of results, allowing you to retrieve subsets of data based on page and page size.
- **`contains()`**: Performs a case-insensitive search to check if a field contains a specific substring.

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
posts = Post.all().contains(title='god').order_by('create_time').paginate(1, 4).to_dict()
```

These methods are particularly useful for data manipulation and debugging, as they provide a simple way to view and interact with your database records.


## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the [Apache-2.0 License](https://github.com/ProdByGodfather/abarorm/blob/main/LICENSE) - see the LICENSE file for details.

## Acknowledgements

- **Python**: The language used for this project.
- **SQLite and Postgresql**: The databases supported by this project.
- **setuptools**: The tool used for packaging and distributing the library.
- **psycopg2-binary**: The PostgreSQL adapter used for connecting to PostgreSQL databases.