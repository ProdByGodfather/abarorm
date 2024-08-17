from orm import SQLiteModel
from fields import CharField, DateTimeField, ForeignKey

# تنظیمات دیتابیس
DATABASE_CONFIG = {
    'sqlite': {
        'db_name': 'example.db',
    }
}

# تعریف مدل‌ها
class Category(SQLiteModel):
    table_name = 'categories'

    title = CharField(max_length=200, unique=True, null=False)

    def __init__(self, **kwargs):
        super().__init__(db_config=DATABASE_CONFIG['sqlite'], **kwargs)

class Post(SQLiteModel):
    table_name = 'posts'

    title = CharField(max_length=100, unique=True, null=False)
    create_time = DateTimeField(auto_now=True)
    category = ForeignKey(to=Category)  # اشاره به مدل Category

    def __init__(self, **kwargs):
        super().__init__(db_config=DATABASE_CONFIG['sqlite'], **kwargs)

# بارگذاری و ایجاد جداول
if __name__ == "__main__":
    # ایجاد جداول
    Category.create_table()
    Post.create_table()

    # ایجاد یک دسته بندی
    Category.create(title='Movies')

    # دریافت دسته بندی برای استفاده در ایجاد پست
    category = Category.get(id=1)
    if category:
        # ایجاد یک پست
        Post.create(title='Godfather', category=category.id)

        # خواندن تمام پست‌ها
        all_posts = Post.all()
        print("All Posts:", [(post.title, post.category) for post in all_posts])

        # استفاده از متد get برای دریافت یک پست بر اساس ID
        post_data = Post.get(id=1)
        if post_data:
            print("Post with ID 1:", post_data.title, post_data.category)

        # فیلتر کردن پست‌ها بر اساس ID دسته بندی
        filtered_posts = Post.filter(category=category.id)
        print("Filtered Posts:", [(post.title, post.category) for post in filtered_posts])

        # به‌روزرسانی یک پست
        Post.update(1, title='Updated Godfather')

        # خواندن پست‌ها پس از به‌روزرسانی
        updated_posts = Post.all()
        print("Updated Posts:", [(post.title, post.category) for post in updated_posts])

        # حذف پست
        # Post.delete(1)

        # خواندن پست‌ها پس از حذف
        final_posts = Post.all()
        print("Final Posts:", [(post.title, post.category) for post in final_posts])
    else:
        print("Category with ID 1 does not exist.")
