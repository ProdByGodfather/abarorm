from orm import SQLiteModel, Field, ForeignKey

# تنظیمات دیتابیس
DATABASE_CONFIG = {
    'sqlite': {
        'db_name': 'example.db',
    }
}

# تعریف مدل‌ها
class Category(SQLiteModel):
    table_name = 'categories'

    title = Field(max_length=200, unique=True)

    def __init__(self):
        super().__init__(DATABASE_CONFIG['sqlite'])

class Post(SQLiteModel):
    table_name = 'posts'

    title = Field(max_length=100, unique=True)
    create_time = Field(auto_now=True)
    category = ForeignKey(Category)  # اشاره به مدل Category

    def __init__(self):
        super().__init__(DATABASE_CONFIG['sqlite'])