# main.py

from orm import SQLiteModel, Field, ForeignKey

# تعریف مدل‌ها
class Category(SQLiteModel):
    table_name = 'categories'
    title = Field(max_length=200, unique=True)

class Post(SQLiteModel):
    table_name = 'posts'
    title = Field(max_length=100, unique=True)
    create_time = Field(auto_now=True)
    category = ForeignKey(Field())

# بارگذاری و ایجاد جداول
if __name__ == "__main__":
    Category.create_table()
    Post.create_table()

    # ایجاد یک دسته بندی
    Category.create(title='Movies')

    # ایجاد یک پست
    category_id = 1  # فرض بر اینکه این ID دسته بندی موجود است
    Post.create(title='Godfather', category=category_id)

    # خواندن تمام پست‌ها
    all_posts = Post.all()
    print("All Posts:", all_posts)

    # فیلتر کردن پست‌ها بر اساس عنوان دسته بندی
    filtered_posts = Post.filter(category=category_id)
    print("Filtered Posts:", filtered_posts)

    # به‌روزرسانی یک پست
    Post.update(1, title='Updated Godfather')

    # خواندن پست‌ها پس از به‌روزرسانی
    updated_posts = Post.all()
    print("Updated Posts:", updated_posts)

    # حذف پست
    Post.delete(1)

    # خواندن پست‌ها پس از حذف
    final_posts = Post.all()
    print("Final Posts:", final_posts)