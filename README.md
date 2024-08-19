# abarorm

| ![abarorm Logo](https://prodbygodfather.github.io/abarorm/images/logo.png) | **abarorm** is a lightweight and easy-to-use Object-Relational Mapping (ORM) library for both SQLite and MySQL databases in Python. It provides a simple and intuitive interface for managing database models and interactions. |
|----------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|

## Features

- Define models using Python classes
- Automatically handle database schema creation and management
- Support for basic CRUD operations
- Foreign key relationships
- Custom field types with validation and constraints
- **New in v1.0.0**: Automatic table creation and updates without needing explicit `create_table()` calls

## Installation

You can install **abarorm** from PyPI using pip:

```bash
pip install abarorm
```
For MySQL support, you also need to install `mysql-connector-python`:
```python
pip install mysql-connector-python
```

## Basic Usage
Here’s a quick overview of how to use **abarorm** to define models and interact with an SQLite or MySQL database.

## Documentation
For detailed documentation, examples, and advanced usage, please visit the [official abarorm documentation website](https://prodbygodfather.github.io/abarorm/).

## Version 1.0.0 Notes
**Automatic Table Management:** Tables are now automatically created or updated based on model definitions without manual intervention.
**Important for Developers:** During development, when adding new fields to models, they will default to `NULL`. It's recommended to recreate the database schema after development is complete to ensure fields have appropriate constraints and default values.

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on GitHub.

## License
This project is licensed under the Apache-2.0 [License](https://github.com/ProdByGodfather/abarorm/blob/main/LICENSE) - see the LICENSE file for details.

## Acknowledgements
**Python:** The language used for this project
**SQLite & MySQL:** The databases supported by this project
**setuptools:** The tool used for packaging and distributing the library