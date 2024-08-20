# Welcome to AbarORM


<div style="display: flex; align-items: center;">
  <div style="flex: 1;">
    <img src="images/logo.png" alt="Logo" style="width: 150px; margin-right: 20px;">
  </div>
  <div style="flex: 2;">
    <p>
     <b>abarorm</b> is a lightweight and easy-to-use Object-Relational Mapping (ORM) library for SQLite, PostgreSQL and MySQL databases in Python. It aims to provide a simple and intuitive interface for managing database models and interactions. 
    </p>
  </div>
</div>


## Features
- Define models using Python classes
- Automatically handle database schema creation and management
- Support for basic CRUD operations
- Foreign key relationships
- Custom field types with validation and constraints
- Easy changeability to start developing

### Supported Databases
![psql](https://img.shields.io/badge/Postgresql-%2320232a.svg?style=for-the-badge&logo=postgresql)
![mysql](https://img.shields.io/badge/mysql-%2320232a.svg?style=for-the-badge&logo=mysql)
![sqlite](https://img.shields.io/badge/sqlite-%2320232a.svg?style=for-the-badge&logo=sqlite)


## Installation

You can install **abarorm** from PyPI using pip:

```bash
pip install abarorm
```

For MySQL support, you also need to install `mysql-connector-python`: (Required)

```bash
pip install mysql-connector-python
```
For PostgreSQL support, install `psycopg2-binary`: (Required)
```bash
pip install psycopg2-binary
```

[Start with abarorm](Introduction.md)