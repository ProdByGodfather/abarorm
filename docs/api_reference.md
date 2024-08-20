# API Reference for AbarORM

This page provides a detailed reference for the classes and methods available in the AbarORM library. The API reference is intended for developers who need a comprehensive understanding of how to use AbarORM's features.

## Classes

### 1. `SQLiteModel`

The `SQLiteModel` class is the base class for defining models that interact with an SQLite database.

#### Methods

- **`class Meta:`**
  - **Description**: Initializes the model with the given database configuration.
  - **Parameters**:
    - `db_config`: Dictionary containing the database configuration.
    - `**kwargs`: Additional keyword arguments.
  

- **`save(self)`**
  - **Description**: Saves the current instance to the database. If it’s a new record, it will be inserted; if it exists, it will be updated.
  - **Parameters**: None

- **`delete(self)`**
  - **Description**: Deletes the current instance from the database.
  - **Parameters**: None

- **`get(cls, id)`**
  - **Description**: Retrieves a single record by its ID.
  - **Parameters**:
    - `id`: The ID of the record to retrieve.

- **`all(cls, order_by)`**
  - **Description**: Retrieves all records from the table and order them.
  - **Parameters**: None

- **`filter(cls, **kwargs)`**
  - **Description**: Retrieves records that match the specified criteria.
  - **Parameters**:
    - `**kwargs`: Criteria for filtering records.

### 2. `MySQLModel`

The `MySQLModel` class is similar to `SQLiteModel` but designed for MySQL databases. It provides the same methods as `SQLiteModel` but interacts with MySQL instead.

#### Methods

The methods for `MySQLModel` and `PostgreSQLModel` are identical to those for `SQLiteModel`, with differences primarily in how they interact with the MySQL database.


### 3. `PostgreSQLModel`

The `PostgreSQLModel` class is similar to `SQLiteModel` but designed for Postgresql databases. It provides the same methods as `SQLiteModel` but interacts with Postgresql instead.

#### Methods

The methods for `MySQLModel` and `PostgreSQLModel` are identical to those for `SQLiteModel`, with differences primarily in how they interact with the MySQL database.

## Fields

### 1. `CharField`

- **Description**: Represents a text field with a maximum length.
- **Parameters**:
  - `max_length`: Maximum number of characters allowed.
  - `unique`: Whether the field must contain unique values.
  - `null`: Whether the field can be `NULL`.
  - `default`: Default value if none is provided.

### 2. `DateTimeField`

- **Description**: Represents a date and time value.
- **Parameters**:
  - `auto_now`: Automatically set to the current date and time on updates.

### 3. `ForeignKey`

- **Description**: Represents a many-to-one relationship between models.
- **Parameters**:
  - `to`: The model this field points to.
  - `on_delete`: Behavior when the referenced record is deleted.

### 4. `BooleanField`

- **Description**: Represents a Boolean value.
- **Parameters**:
  - `default`: Default value if none is provided.
  - `null`: Whether the field can be `NULL`.

### 5. `IntegerField`

- **Description**: Represents an integer value.
- **Parameters**:
  - `default`: Default value if none is provided.
  - `null`: Whether the field can be `NULL`.

### 6. `FloatField`

- **Description**: Represents a floating-point number.
- **Parameters**:
  - `default`: Default value if none is provided.
  - `null`: Whether the field can be `NULL`.

### 7. `EmailField`

- **Description**: Represents an email address.
- **Parameters**:
  - `max_length`: Maximum number of characters allowed.
  - `unique`: Whether the field must contain unique values.

### 8. `URLField`

- **Description**: Represents a URL.
- **Parameters**:
  - `max_length`: Maximum number of characters allowed.

### 9. `TextField`

- **Description**: Represents a large text field for storing long texts.
- **Parameters**:
  - `null`: Whether the field can be `NULL`.

### 10. `DecimalField`

- **Description**: Represents a decimal number with fixed precision.
- **Parameters**:
  - `max_digits`: Maximum number of digits allowed.
  - `decimal_places`: Number of decimal places to store.
  - `default`: Default value if none is provided.

## Query Methods

### 1. `create(cls, **kwargs)`

- **Description**: Creates a new record with the specified data.
- **Parameters**:
  - `**kwargs`: Data for the new record.

### 2. `update(cls, id, **kwargs)`

- **Description**: Updates an existing record with new data.
- **Parameters**:
  - `id`: ID of the record to update.
  - `**kwargs`: New data for the record.

### 3. `delete(cls, id)`

- **Description**: Deletes a record by its ID.
- **Parameters**:
  - `id`: ID of the record to delete.

## Summary

This API reference provides an overview of the core classes, methods, and fields available in AbarORM. For more detailed examples and use cases, refer to the [Basic Usage](basic_usage.md) section.

If you have any questions or need further assistance, please check the [Documentation](index.md) or reach out to the community via our [GitHub repository](https://github.com/prodbygodfather/abarorm).

Happy coding with AbarORM!
