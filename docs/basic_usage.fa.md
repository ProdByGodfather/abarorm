---
title: "استفاده پایه از AbarORM"
---

# استفاده پایه از AbarORM

## مقدمه

در این بخش، نحوه استفاده پایه از AbarORM را پوشش خواهیم داد، از جمله نحوه تعریف مدل‌ها، ایجاد جداول و انجام عملیات CRUD پایه. این راهنما فرض می‌کند که شما AbarORM را نصب کرده‌اید و با زبان برنامه‌نویسی پایتون آشنا هستید.

## گام اول: تعریف مدل‌ها

برای شروع استفاده از AbarORM، ابتدا باید مدل‌های پایگاه داده خود را تعریف کنید. هر مدل معادل یک جدول در پایگاه داده شماست. در اینجا نحوه تعریف یک مدل ساده آورده شده است:

### مثال: تعریف مدل‌ها

```python
from abarorm import SQLiteModel
from abarorm.fields.sqlite import CharField, DateTimeField, ForeignKey
from abarorm.fields import psql

# Database configuration
DATABASE_CONFIG = {
    'sqlite': {
        'db_name': 'example.db',  # Name of the SQLite database file
    },
    # This connection string model is used to connect to postgresql database
    # which we have not used in this example
    'postgresql': {
        'host': 'localhost',
        'user': 'hoopad',
        'password': 'db_password',
        'database': 'example_db',  
        'port': 5432,
    }
}

# Define the Category model
class Category(SQLiteModel):
    title = CharField(max_length=200, unique=True)
    class Meta:
        db_config = DATABASE_CONFIG['sqlite']
        table_name = 'categories'  # Name of the table for storing the Category model data in SQLite


# Define the Post model
class Post(SQLiteModel):
    title = psql.CharField(max_length=100, unique=True)
    create_time = psql.DateTimeField(auto_now=True)
    category = psql.ForeignKey(Category)
    class Meta:
        db_config = DATABASE_CONFIG['postgresql']
```
!!! info inline end "توجه!"

    فیلدهای موجود در پایگاه داده PostgreSQL و SQLite از نظر ساختاری یکسان هستند و برای استفاده به روش مشابه طراحی شده اند، اما برای استفاده از هر یک از پایگاه داده ها، باید از فیلدهایی از همان پایگاه داده در مدل های خود استفاده کنید. به عنوان مثال، مسیر فیلدهای `sqlite`: `abarorm.fields.sqlite` و مسیر فیلدهای `postgresql` به صورت: `abarorm.fields.psql` است.

در مثال بالا:

- `Category` و `Post` دو مدل هستند که معادل جداول پایگاه داده هستند.
- هر کلاس از `SQLiteModel` ارث‌بری می‌کند و فیلدها با استفاده از انواع فیلدهای داخلی AbarORM تعریف می‌شوند.

## گام دوم: انجام عملیات CRUD
بعد از ایجاد جداول، می‌توانید عملیات CRUD (ایجاد، خواندن، به‌روزرسانی، حذف) را روی مدل‌ها انجام دهید.

### ایجاد رکوردها

برای اضافه کردن رکوردهای جدید به پایگاه داده، از متد `create` استفاده کنید:


```python
# Add a new category
Category.create(title='Movies')

# Add a new post
category = Category.get(id=1)  # Fetch the category with ID 1
if category:
    Post.create(title='Godfather', category=category.id)
```
### خواندن رکوردها

برای بازیابی رکوردها از پایگاه داده، از متدهای `all`، `get` یا `filter` استفاده کنید:

```python
# Retrieve all posts
all_posts = Post.all()
print("All posts:", all_posts)
# Retrieve a specific post
post_data = Post.get(id=1)
if post_data:
    print("Post with ID 1:", post_data)
```
### فیلتر کردن رکوردها

متد `filter()` به شما امکان می‌دهد رکوردها را بر اساس معیارهای خاص فیلتر کنید. می‌توانید از آرگومان‌های کلیدی برای فیلتر کردن بر اساس مقادیر فیلدها و همچنین مرتب‌سازی نتایج با استفاده از `order_by` استفاده کنید.
```python
# Filter posts by category ID and order by creation time
filtered_posts = Post.filter(category=category.id)
```
#### فیلتر پیشرفته

همچنین می‌توانید از عبارات جستجو خاص مانند `__gte` (بزرگ‌تر یا مساوی) و `__lte` (کوچک‌تر یا مساوی) برای انجام جستجوهای پیچیده‌تر استفاده کنید:

```python
# Retrieve posts created after a specific date
filtered_posts = Post.filter(create_time__gte='2024-01-01 00:00:00')
```

### به‌روزرسانی رکوردها

برای به‌روزرسانی رکوردهای موجود، از متد `update` استفاده کنید:


```python
# Update a post
Post.update(id=1, title='The Godfather Part II')
```
همچنین می‌توانید فیلدی را همزمان با دریافت آن به‌روزرسانی کنید:


```python
category = Category.get(id=id)
category.title = title
category.save()
```
### حذف رکوردها

برای حذف رکوردها، از متد `delete`
 استفاده کنید:
```python
# Delete a post
Post.delete(id=1)
# Likewise, deletion based on duplicate fields
Post.delete(title='godfather')
```
### مدیریت روابط

AbarORM از روابط کلید خارجی بین مدل‌ها پشتیبانی می‌کند. در مثال ارائه شده، مدل `Post` یک رابطه کلید خارجی با مدل `Category` دارد. این امکان را به شما می‌دهد که ساختارهای داده پیچیده‌تری ایجاد کرده و داده‌های مرتبط را به طور کارآمد مدیریت کنید.

### مثال: دسترسی به داده‌های مرتبط

```python
# Access the category of a post
post = Post.get(id=1)
if post:
    category = Category.get(id=post.category)
    print("Post Category:", category.title)
```


### تبدیل به دیکشنری و شمارش رکوردها 
پس از انجام عملیات روی مدل، می توانید رکوردها را با استفاده از متد `to_dict()` به دیکشنری تبدیل کنید و با استفاده از متد `count()` تعداد رکوردها را بشمارید.

#### `to_dict` متد
متد `to_dict()` یک نمونه مدل را به دیکشنری تبدیل می‌کند و دستکاری و سریال‌سازی داده‌ها را آسان‌تر می‌کند.

**مثال:**
```python
# Retrieve a post by ID
post = Post.get(id=1)

# Convert the post to a dictionary
post_dict = post.all().to_dict()
print(post_dict)
# Output: [{'id': 1, 'title': 'Godfather', 'create_time': '2024-01-01 12:00:00', ...}]
```

#### `count` متد
متد `count()` به شما امکان می دهد تعداد رکوردهای جدول یک مدل را بدست آورید.

**مثال:**
```python
# Count the number of posts in the database
num_posts = Post.count()
print(num_posts)  # Output: 10 (if there are 10 posts in the database)
```

#### `first()`, `last()`, `exists()`, `order_by()`, `paginate()` و `contains()`
- `first():` اولین نتیجه یا None را در صورت عدم وجود نتیجه برمی گرداند.
- `last():` آخرین نتیجه یا None را در صورت عدم وجود نتیجه برمی گرداند.
- `exists():` بررسی می کند که آیا رکوردی در `QuerySet` وجود دارد یا خیر.
- `paginate():` صفحه بندی نتایج را کنترل می کند و به شما امکان می دهد زیرمجموعه هایی از داده ها را بر اساس اندازه صفحه و صفحه بازیابی کنید.
- `contains():` یک جستجوی غیر حساس به حروف بزرگ و کوچک برای بررسی اینکه آیا یک فیلد حاوی یک زیررشته خاص است انجام می دهد.


**نمونه:**
```python
# Check if any posts exist
exists = Post.all().exists()

# Get the first post
first_post = Post.all().first()

# Get the last post
last_post = Post.all().last()

# Paginate the results
paginated_posts = Post.all().paginate(1, 5)  # Page 1, 5 results per page

# Searching with one field
searched_posts = Post.all().contains(title='god')

# Using multiple querysets in one query
posts = Post.all().contains(title='God').order_by('create_time').paginate(1, 4).to_dict()
```

این روش ها به ویژه برای دستکاری داده ها و اشکال زدایی مفید هستند، زیرا روشی ساده برای مشاهده و تعامل با سوابق پایگاه داده شما ارائه می دهند.

## خلاصه

این راهنما استفاده پایه از AbarORM را پوشش داد، از جمله تعریف مدل‌ها، ایجاد جداول و عملیات CRUD. برای ویژگی‌ها و پیکربندی‌های پیشرفته‌تر، به بخش [Field Types](/abarorm/field_types.fa) مراجعه کنید.

