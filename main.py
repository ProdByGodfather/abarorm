from db import Category, Post

# بارگذاری و ایجاد جداول
if __name__ == "__main__":
    # ایجاد جداول
    Category().create_table()
    Post().create_table()

    # ایجاد یک دسته بندی
    category = Category()
    category.create(title='Movidfadfes')

    # ایجاد یک پست
    category_id = 1  # فرض بر اینکه این ID دسته بندی موجود است
    post = Post()
    post.create(title='Godadsffather', category=category_id)

    # خواندن تمام پست‌ها
    all_posts = Post.all()
    print("All Posts:", all_posts)

    # فیلتر کردن پست‌ها بر اساس عنوان دسته بندی
    filtered_posts = Post.filter(category=category_id)
    print("Filtered Posts:", filtered_posts)

    # به‌روزرسانی یک پست
    post.update(1, title='Updated Godfatsgsgher')

    # خواندن پست‌ها پس از به‌روزرسانی
    updated_posts = Post.all()
    print("Updated Posts:", updated_posts)

    # حذف پست
    post.delete(1)

    # خواندن پست‌ها پس از حذف
    final_posts = Post.all()
    print("Final Posts:", final_posts)