# مدل سازی SQLite

در این بخش نحوه تعریف مدل‌ها برای SQLite با استفاده از کتابخانه AbarORM را بررسی خواهیم کرد.

## مثال پایه

برای استفاده از SQLite با AbarORM، باید مدل‌های خود را از `SQLiteModel` ارث بری کنید. در اینجا یک مثال پایه آورده شده است:

```python
from abarorm import SQLiteModel
from abarorm.fields import CharField, DateTimeField, ForeignKey

DATABASE_CONFIG = {
    'sqlite': {
        'db_name': 'example.db',  # Name of the SQLite database file
    }
}

class Category(SQLiteModel):
    title = CharField(max_length=200, unique=True)
    class Meta:
        db_config = DATABASE_CONFIG['sqlite']
        table_name = 'categories'  # Name of the table for storing the Category model data in SQLite


class Post(SQLiteModel):
    title = CharField(max_length=100, unique=True)
    create_time = DateTimeField(auto_now=True)
    category = ForeignKey(Category)
    class Meta:
        db_config = DATABASE_CONFIG['sqlite'])
```
## مدیریت خودکار جداول
در نسخه جدید AbarORM، دیگر نیازی به ایجاد دستی جداول نیست. این کتابخانه به طور خودکار ایجاد و مدیریت جداول شما را بر اساس تعاریف مدل انجام می‌دهد. به این معنی که به محض شروع تعامل با مدل‌های خود، AbarORM اطمینان حاصل می‌کند که اگر جداول مربوطه از قبل وجود نداشته باشند، ایجاد می‌شوند. با این حال، شما می‌توانید به صورت دستی نام جداول را با تعریف متغیر `table_name` در کلاس Meta مدیریت کنید.

## بروزرسانی خودکار اسکیمای پایگاه داده
AbarORM همچنین از بروزرسانی خودکار اسکیما پشتیبانی می‌کند. اگر فیلدهای جدیدی به مدل‌های خود اضافه کنید در حالی که اپلیکیشن در حال اجرا است، AbarORM به طور خودکار اسکیما پایگاه داده را برای منعطف کردن این تغییرات به روز خواهد کرد. این امر نیاز به اسکریپت‌های مهاجرت دستی یا بازسازی پایگاه داده را از بین می‌برد.

???+ هشدار
    اگرچه بروزرسانی‌های اسکیما به طور خودکار انجام می‌شود، توصیه می‌شود که پس از تکمیل توسعه، اسکیما پایگاه داده خود را دوباره ایجاد کنید تا از اعمال صحیح تمامی فیلدها و محدودیت‌ها اطمینان حاصل کنید. این کمک می‌کند تا از مشکلات احتمالی جلوگیری شود و اطمینان حاصل کنید که پایگاه داده شما قبل از حرکت به سمت تولید در وضعیت ثابتی قرار دارد.

## CRUD
در مدل‌سازی و استفاده از پایگاه داده‌ها، هیچ تفاوتی در نوع و روش CRUD وجود ندارد و برای ایجاد آن‌ها می‌توانید به صفحه [استفاده پایه - CRUD](/basic_usage/#step-3-perform-crud-operations) مراجعه کنید.