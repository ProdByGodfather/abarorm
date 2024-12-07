---
title: "Welcome to AbarORM"
---


# Welcome to AbarORM


<div style="display: flex; align-items: center;">
  <div style="flex: 1;">
    <img src="images/logo.png" alt="Logo" style="width: 150px; margin-right: 20px;">
  </div>
  <div style="flex: 2;">
    <p>
     <b>abarorm</b> is a lightweight and easy-to-use Object-Relational Mapping (ORM) library for SQLite and PostgreSQL databases in Python. It aims to provide a simple and intuitive interface for managing database models and interactions. 
    </p>
  </div>
</div>


## Features
- Define models using Python classes.
- Automatically handle database schema creation and management.
- Support for basic CRUD (Create, Read, Update, Delete) operations.
- Manage foreign key relationships effortlessly.
- Custom field types with validation and constraints.
- **New in v1.0.0**: Automatic table creation and updates.
- **New in v2.0.0**: Added support for PostgreSQL databases.
- **New in v2.0.0**: Ordering by fields in the `all()` method.
- **New in v3.0.0**: Fixed table naming bugs to ensure consistent naming conventions.
- **New in v3.0.0**: Updated return values for methods to improve clarity and usability.
- **New in v3.0.0**: Enhanced `filter` method now supports `order_by` for ordering.
- **New in v3.2.0**: Added `__gte` and `__lte` functionality in the filter section.
- **New in v4.0.0**: Added `__repr__`, count, and `to_dict` methods for easier data manipulation and debugging.
- **New in v4.2.3**: Added `first()`, `last()`, `exists()`, and `paginate()` methods to the QuerySet class for more powerful querying capabilities.
- **New in v5.0.0**: Fix `PostgreSQL` Bugs and structure.





### Supported Databases
![psql](https://img.shields.io/badge/Postgresql-%2320232a.svg?style=for-the-badge&logo=postgresql)
![sqlite](https://img.shields.io/badge/sqlite-%2320232a.svg?style=for-the-badge&logo=sqlite)


## Installation

You can install **abarorm** from PyPI using pip:

```bash
pip install abarorm
```


For PostgreSQL support, install `psycopg2-binary`: (Required)
```bash
pip install psycopg2-binary
```

[Start with abarorm](/abarorm/Introduction)