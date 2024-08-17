# main.py

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

# بارگذاری و ایجاد جداول
if __name__ == "__main__":
    # ایجاد جداول
    Category().create_table()
    Post().create_table()

    # ایجاد یک دسته بندی
    category = Category()
    category.create(title='Movies')

    # ایجاد یک پست
    category_id = 1  # فرض بر اینکه این ID دسته بندی موجود است
    post = Post()
    post.create(title='Godfather', category=category_id)

    # خواندن تمام پست‌ها
    all_posts = Post.all()
    print("All Posts:", all_posts)

    # استفاده از متد get برای دریافت یک پست بر اساس ID
    post_data = Post.get(id=1)
    print("Post with ID 1:", post_data)

    # فیلتر کردن پست‌ها بر اساس عنوان دسته بندی
    filtered_posts = Post.filter(category=category_id)
    print("Filtered Posts:", filtered_posts)

    # به‌روزرسانی یک پست
    post.update(1, title='Updated Godfather')

    # خواندن پست‌ها پس از به‌روزرسانی
    updated_posts = Post.all()
    print("Updated Posts:", updated_posts)

    # حذف پست
    post.delete(1)

    # خواندن پست‌ها پس از حذف
    final_posts = Post.all()
    print("Final Posts:", final_posts)