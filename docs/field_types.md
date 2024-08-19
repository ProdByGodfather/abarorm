# Field Types in AbarORM

In AbarORM, fields define the types of data stored in your database models. Each field type represents a specific kind of data and provides options for validation and constraints. This guide covers the available field types and their usage.

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