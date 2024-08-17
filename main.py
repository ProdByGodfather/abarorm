import sqlite3
import psycopg2
from config import DATABASE_CONFIG

class BaseModel:
    table_name = ''
    
    @classmethod
    def connect(cls):
        raise NotImplementedError("Connect method must be implemented.")
    
    @classmethod
    def create_table(cls):
        raise NotImplementedError("Create table method must be implemented.")
    
    @classmethod
    def all(cls):
        conn = cls.connect()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {cls.table_name}")
        results = cursor.fetchall()
        conn.close()
        return results
    
    @classmethod
    def filter(cls, **kwargs):
        conn = cls.connect()
        cursor = conn.cursor()
        query = f"SELECT * FROM {cls.table_name} WHERE " + " AND ".join([f"{k} = ?" for k in kwargs.keys()])
        cursor.execute(query, tuple(kwargs.values()))
        results = cursor.fetchall()
        conn.close()
        return results
    
    @classmethod
    def create(cls, **kwargs):
        conn = cls.connect()
        cursor = conn.cursor()
        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join(['?'] * len(kwargs))
        cursor.execute(f"INSERT INTO {cls.table_name} ({columns}) VALUES ({placeholders})", tuple(kwargs.values()))
        conn.commit()
        conn.close()
    
    @classmethod
    def update(cls, id, **kwargs):
        conn = cls.connect()
        cursor = conn.cursor()
        set_clause = ', '.join([f"{k} = ?" for k in kwargs.keys()])
        cursor.execute(f"UPDATE {cls.table_name} SET {set_clause} WHERE id = ?", (*kwargs.values(), id))
        conn.commit()
        conn.close()
    
    @classmethod
    def delete(cls, id):
        conn = cls.connect()
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {cls.table_name} WHERE id = ?", (id,))
        conn.commit()
        conn.close()

class SQLiteModel(BaseModel):
    db_name = DATABASE_CONFIG['sqlite']['db_name']
    
    @classmethod
    def connect(cls):
        return sqlite3.connect(cls.db_name)
    
    @classmethod
    def create_table(cls):
        conn = cls.connect()
        cursor = conn.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {cls.table_name} (id INTEGER PRIMARY KEY, name TEXT)")
        conn.commit()
        conn.close()

class PostgreSQLModel(BaseModel):
    db_name = DATABASE_CONFIG['postgresql']['db_name']
    user = DATABASE_CONFIG['postgresql']['user']
    password = DATABASE_CONFIG['postgresql']['password']
    host = DATABASE_CONFIG['postgresql']['host']
    
    @classmethod
    def connect(cls):
        return psycopg2.connect(dbname=cls.db_name, user=cls.user, password=cls.password, host=cls.host)
    
    @classmethod
    def create_table(cls):
        conn = cls.connect()
        cursor = conn.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {cls.table_name} (id SERIAL PRIMARY KEY, name TEXT)")
        conn.commit()
        conn.close()


# انتخاب دیتابیس بر اساس پیکربندی
database_type = DATABASE_CONFIG['database_type']

if database_type == 'sqlite':
    class MyModel(SQLiteModel):
        table_name = 'my_models'
elif database_type == 'postgresql':
    class MyModel(PostgreSQLModel):
        table_name = 'my_models'

else:
    raise ValueError("Unsupported database type.")

if __name__ == "__main__":
    MyModel.create_table()
    
    # ایجاد یک مدل جدید
    MyModel.create(name='Test Model')
    
    # خواندن تمام مدل‌ها
    all_models = MyModel.all()
    print("All Models:", all_models)
    
    # فیلتر کردن مدل‌ها
    filtered_models = MyModel.filter(name='Test Model')
    print("Filtered Models:", filtered_models)
    
    # به‌روزرسانی مدل
    MyModel.update(1, name='Updated Model')
    
    # خواندن مدل‌ها پس از به‌روزرسانی
    updated_models = MyModel.all()
    print("Updated Models:", updated_models)
    
    # حذف مدل
    MyModel.delete(1)
    
    # خواندن مدل‌ها پس از حذف
    final_models = MyModel.all()
    print("Final Models:", final_models)