---
title: "Field Types in AbarORM"
---


# Field Types in AbarORM

In AbarORM, fields define the types of data stored in your database models. Each field type represents a specific kind of data and provides options for validation and constraints. This guide covers the available field types and their usage.

In AbarORM, fields define the type of data stored in your database models. Each field type represents a specific type of data and provides options for validation and constraints. In this guide, we will explore the available field types and how to use them.

The fields in PostgreSQL and SQLite databases are structurally identical and are designed to be used in a similar way, but to use either database, you must use fields from the same database in your models. For example, the path to fields

- **sqlite**: `abarorm.fields.sqlite`
- **postgresql**: `abarorm.fields.psql`

## Basic Field Types

### 1. CharField

- **Description**: Represents a text field with a maximum length.
- **Parameters**:
  - `max_length`: The maximum number of characters allowed.
  - `unique`: If `True`, the field must contain unique values across the table.
  - `null`: If `True`, the field can contain `NULL` values.
  - `default`: The default value if none is provided.
- **Example**:
  ```python
  title = CharField(max_length=100, unique=True)
  ```
### 2. DateTimeField

- **Description:** Represents a date and time value.
- **Parameters:**
    - `auto_now:` If True, the field will be automatically set to the current date and time whenever the record is updated.
    - `auto_now:` If True, the field will be automatically set to the current date and time whenever the record is created.
    - `auto_now_add:` 
- **Example:**
  ```python
  create_time = DateTimeField(auto_now=True)
  ```
### 3. ForeignKey

- **Description:** Represents a many-to-one relationship between models.
- **Parameters:**
    - `to:` The model that this field points to.
    - `on_delete:` Defines the behavior when the referenced record is deleted. Common options include:
    - `CASCADE:` Automatically delete records that reference the deleted record.
    - `SET NULL:` Set the field to NULL when the referenced record is deleted.
    - `PROTECT:` Prevent deletion of the referenced record by raising an error.
    - `SET_DEFAULT:` Set the field to a default value when the referenced record is deleted.
    - `DO_NOTHING:` Do nothing and leave the field unchanged.

- **Example:**
  ```python
  category = ForeignKey(Category, on_delete='CASCADE')
  ```

### 4. BooleanField
- **Description:** Represents a Boolean value (`True` or `False`).
- **Parameters:**
    - `default:` The default value for the field if none is provided.
    - `null:` If True, the field can contain NULL values.
- **Example:**
  ```python
  is_active = BooleanField(default=True)
  ```

### 5. IntegerField
- **Description:** Represents an integer value.
- **Parameters:**
    - `default:` The default value for the field if none is provided.
    - `null:` If True, the field can contain NULL values.
- **Example:**
    ```python
    age = IntegerField(default=0)
    ```

### 6. FloatField
- **Description:** Represents a floating-point number.
- **Parameters:**
    - `default:` The default values for the field if none is provided.
    - `null:` If True, the field can contain NULL values.
- **Example:**
```python
price = FloatField(default=0.0)
```

### 7. DecimalField
- **Description:** Represents a decimal number with fixed precision and scale.
- **Parameters:**
    - `max_digits:` The maximum number of digits (including both integer and decimal places).
    - `decimal_places:` The number of decimal places.
    - `default:` The default values for the field if none is provided.
    - `null:` If True, the field can contain NULL values.
- **Example:**
```python
salary = DecimalField(max_digits=10, decimal_places=2, default=0.00)
```

### 8. DateField
- **Description:** Represents a decimal number with fixed precision and scale.
- **Parameters:**
    - `default:` The default values for the field if none is provided.
    - `null:` If True, the field can contain NULL values.
- **Example:**
```python
birth_date = DateField(default='2000-01-01')
```

### 9. TimeField
- **Description:** Represents a decimal number with fixed precision and scale.
- **Parameters:**
    - `default:` The default values for the field if none is provided.
    - `null:` If True, the field can contain NULL values.
- **Example:**
```python
meeting_time = TimeField(default='09:00:00')
```

### 10. TextField
- **Description:** Represents a decimal number with fixed precision and scale.
- **Parameters:**
    - `default:` The default values for the field if none is provided.
    - `null:` If True, the field can contain NULL values.
- **Example:**
```python
description = TextField(null=True)
```