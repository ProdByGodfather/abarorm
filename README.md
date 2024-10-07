# abarorm

| ![abarorm Logo](https://prodbygodfather.github.io/abarorm/images/logo.png) | **abarorm** is a lightweight and easy-to-use Object-Relational Mapping (ORM) library for SQLite, MySQL, and PostgreSQL databases in Python. It provides a simple and intuitive interface for managing database models and interactions. |
|----------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## Features

- Define models using Python classes
- Automatically handle database schema creation and management
- Support for basic CRUD operations
- Foreign key relationships
- Custom field types with validation and constraints
- **New in v1.0.0**: Automatic table creation and updates without needing explicit `create_table()` calls
- **New in v2.0.0**: Added support for PostgreSQL databases
- **New in v2.0.0**: Ordering by fields on `all()` method
- **New in v3.0.0**: Fixed table naming bugs to ensure consistent naming conventions
- **New in v3.0.0**: Updated return values for methods to improve clarity and usability
- **New in v3.0.0**: Enhanced `filter` method now supports `order_by` functionality for result ordering


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


## Basic Usage
Here’s a quick overview of how to use **abarorm** to define models and interact with an SQLite or MySQL database.

## Documentation
For detailed documentation, examples, and advanced usage, please visit the [official abarorm documentation website](https://prodbygodfather.github.io/abarorm/).

## Version 3.0.0 Notes
- Fixed Table Naming: Resolved issues related to inconsistent table naming conventions.
- Return Values Updated: Methods now return values that enhance clarity and usability.
- Filter Enhancements: The `filter` method now includes support for `order_by`, allowing for more flexible queries.
**Important for Developers:** When adding new fields to models, they will default to `NULL`. It’s recommended to recreate the database schema after development is complete to ensure fields have appropriate constraints and default values.

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on GitHub.

## License
This project is licensed under the Apache-2.0 [License](https://github.com/ProdByGodfather/abarorm/blob/main/LICENSE) - see the LICENSE file for details.

## Acknowledgements
**Python:** The language used for this project
**SQLite & MySQL:** The databases supported by this project
**setuptools:** The tool used for packaging and distributing the library
**psycopg2-binary:** The PostgreSQL adapter used for connecting to PostgreSQL databases
