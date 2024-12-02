---
title: "خانه"
---

# خوش آمدید به AbarORM


<div style="display: flex; align-items: center;"> <div style="flex: 1;"> <img src="../images/logo.png" alt="لوگو" style="width: 150px; margin-right: 20px;"> </div> <div style="flex: 2;"> <p> <b>abarorm</b> یک کتابخانه سبک و آسان برای استفاده از نگاشت شیء-رابطه‌ای (ORM) برای پایگاه‌داده‌های SQLite، PostgreSQL و MySQL در پایتون است. هدف آن ارائه یک رابط ساده و شهودی برای مدیریت مدل‌های پایگاه‌داده و تعاملات است. </p> </div> </div>



## ویژگی‌ها
- تعریف مدل‌ها با استفاده از کلاس‌های پایتون.
- مدیریت خودکار ایجاد و مدیریت طرح پایگاه‌داده.
- پشتیبانی از عملیات CRUD (ایجاد، خواندن، به‌روزرسانی، حذف) پایه.
- مدیریت روابط کلید خارجی به سادگی.
- انواع فیلد سفارشی با اعتبارسنجی و محدودیت‌ها.
- **جدید در v1.0.0**:  ایجاد و به‌روزرسانی جدول به‌صورت خودکار.
- **جدید در v2.0.0**: افزودن پشتیبانی از پایگاه‌داده‌های PostgreSQL.
- **جدید در v2.0.0**: مرتب‌سازی بر اساس فیلدها در متد `all()`.
- **جدید در v3.0.0**: رفع اشکالات نام‌گذاری جدول برای اطمینان از سازگاری نام‌ها.
- **جدید در v3.0.0**: به‌روزرسانی مقادیر برگشتی متدها برای بهبود وضوح و قابلیت استفاده.
- **جدید در v3.0.0**: متد `filter` بهبود یافته اکنون از `order_by` برای مرتب‌سازی پشتیبانی می‌کند.
- **جدید در v3.2.0**: افزودن قابلیت `__gte` و `__lte` در بخش فیلتر.
- **جدید در v4.0.0**: روش های `__repr__` ، `count` و `to_dict`  برای دستکاری داده ها و اشکال زدایی آسان تر اضافه شد.
- **جدید در v4.2.3**: متدهای `first()` ، `last()` ، `exists()` و `paginate()` به کلاس `QuerySet` برای قابلیت های جستجوی قدرتمندتر اضافه شده است.

### پایگاه‌داده‌های پشتیبانی‌شده

![psql](https://img.shields.io/badge/Postgresql-%2320232a.svg?style=for-the-badge&logo=postgresql)
![mysql](https://img.shields.io/badge/mysql-%2320232a.svg?style=for-the-badge&logo=mysql)
![sqlite](https://img.shields.io/badge/sqlite-%2320232a.svg?style=for-the-badge&logo=sqlite)


## نصب

شما می‌توانید abarorm را از PyPI با استفاده از `pip` نصب کنید:

```bash
pip install abarorm
```

برای پشتیبانی از MySQL، شما همچنین نیاز به نصب `mysql-connector-python` دارید: (ضروری)

```bash
pip install mysql-connector-python
```
برای پشتیبانی از PostgreSQL، `psycopg2-binary` را نصب کنید: (ضروری)

```bash
pip install psycopg2-binary
```

[با abarorm شروع کنید](/abarorm/Introduction.fa)