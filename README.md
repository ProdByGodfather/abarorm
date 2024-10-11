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

## Basic Usage
Here’s a quick overview of how to use **abarorm** to define models and interact with an SQLite or MySQL database.
```python
from abarorm import SQLiteModel, MySQLModel, PostgreSQLModel
from abarorm.fields import CharField, DateTimeField, ForeignKey

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

# Define the Category model for SQLite
class Category(SQLiteModel):
    class Meta:
        db_config = DATABASE_CONFIG['sqlite']
        table_name = 'categories'  # Name of the table for storing the Category model data in SQLite

    # Define the fields of the Category model
    title = CharField(max_length=200, null=False)  # Title of the category, must be unique and not null
    create_time = DateTimeField(auto_now=True, auto_now_add=True)  # Creation time of the category, automatically set to current datetime
    update_time = DateTimeField(auto_now=True)  # Update time of the category, automatically set to current datetime


# Define the Post model for SQLite
class Post(MySQLModel):
    class Meta:
        db_config = DATABASE_CONFIG['mysql']

    # Define the fields of the Post model
    title = CharField(max_length=100, null=False)  # Title of the post, must be unique and not null
    create_time = DateTimeField(auto_now=True)  # Creation time of the post, automatically set to current datetime
    category = ForeignKey(to=Category)  # Foreign key referring to the Category model


# Main execution block
if __name__ == "__main__":

    # Create a new category
    Category.create(title='Movies')  # Add a new category with title 'Movies'

    # Retrieve the category for use in creating a post
    category = Category.get(id=1)  # Fetch the category with ID 1
    if category:
        # Create a new post
        Post.create(title='Godfather', category=category.id)  # Add a new post with title 'Godfather' and associate it with the fetched category

        # Read all posts
        all_posts = Post.all()  # Retrieve all posts from the database
        all_categories = Category.all()  # Retrieve all categories from the database
        print("All Posts:", [(post.title, post.category) for post in all_posts])  # Print all posts with their titles and associated categories
        print("All Categories:", [(cat.title, cat.create_time, cat.update_time) for cat in all_categories])  # Print all categories with their details

        # Use the get method to retrieve a post by ID
        post_data = Post.get(id=1)  # Fetch the post with ID 1
        if post_data:
            print("Post with ID 1:", post_data.title, post_data.category)  # Print the title and category of the post with ID 1

        # Filter posts based on category ID
        filtered_posts = Post.filter(category=category.id, order_by='-create_time')  # Retrieve all posts associated with the specified category ID
        print("Filtered Posts:", [(post.title, post.category) for post in filtered_posts])  # Print posts filtered by category

        # Update an existing post
        Post.update(1, title='Updated Godfather')  # Update the title of the post with ID 1 to 'Updated Godfather'

        # Read all posts after updating
        updated_posts = Post.all()  # Retrieve all posts from the database after the update
        print("Updated Posts:", [(post.title, post.category) for post in updated_posts])  # Print all posts with updated details

        # Delete a post
        Post.delete(1)  # Delete the post with ID 1

        # Read all posts after deletion
        final_posts = Post.all(order_by='create_time')  # Retrieve all posts from the database after deletion
        print("Final Posts:", [(post.title, post.category) for post in final_posts])  # Print all remaining posts

    else:
        print("Category with ID 1 does not exist.")  # Print a message if the category with ID 1 does not exist
```

### Version 3.0.0

- **Fixed Table Naming**: Resolved issues related to inconsistent table naming conventions.
- **Return Values Updated**: Methods now return values that enhance clarity and usability.
- **Filter Enhancements**: The `filter` method now includes support for `order_by`, allowing for more flexible queries.

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