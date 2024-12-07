from abarorm import SQLiteModel, MySQLModel, PostgreSQLModel
from abarorm.fields.sqlite import CharField, DateTimeField, ForeignKey

# Database configuration
DATABASE_CONFIG = {
    'sqlite': {
        'db_name': 'example.db',  # Name of the SQLite database file
    },
    'mysql': {
        'host': 'localhost',
        'user': 'your_mysql_user',
        'password': 'your_mysql_password',
        'database': 'example_db',
    },
    'postgresql': {
        'host': 'localhost',
        'user': 'your_pg_user',
        'password': 'your_pg_password',
        'database': 'example_db',
    }
}

# Define the Category model for SQLite
class Category(SQLiteModel):
    class Meta:
        db_config = DATABASE_CONFIG['sqlite']
        table_name = 'categories'  # Name of the table for storing the Category model data in SQLite

    # Define the fields of the Category model
    title = CharField(max_length=200, null=False)  # Title of the category, must be unique and not null
    create_time = DateTimeField(auto_now=True, auto_now_add=True)  # Creation time of the category, automatically set to current datetime
    update_time = DateTimeField(auto_now=True)  # Update time of the category, automatically set to current datetime


# Define the Post model for SQLite
class Post(MySQLModel):
    class Meta:
        db_config = DATABASE_CONFIG['mysql']

    # Define the fields of the Post model
    title = CharField(max_length=100, null=False)  # Title of the post, must be unique and not null
    create_time = DateTimeField(auto_now=True)  # Creation time of the post, automatically set to current datetime
    category = ForeignKey(to=Category)  # Foreign key referring to the Category model


# Main execution block
if __name__ == "__main__":

    # Create a new category
    Category.create(title='Movies')  # Add a new category with title 'Movies'

    # Retrieve the category for use in creating a post
    category = Category.get(id=1)  # Fetch the category with ID 1
    if category:
        # Create a new post
        Post.create(title='Godfather', category=category.id)  # Add a new post with title 'Godfather' and associate it with the fetched category

        # Read all posts
        all_posts = Post.all()  # Retrieve all posts from the database
        all_categories = Category.all()  # Retrieve all categories from the database
        print("All Posts:", [(post.title, post.category) for post in all_posts])  # Print all posts with their titles and associated categories
        print("All Categories:", [(cat.title, cat.create_time, cat.update_time) for cat in all_categories])  # Print all categories with their details

        # Use the get method to retrieve a post by ID
        post_data = Post.get(id=1)  # Fetch the post with ID 1
        if post_data:
            print("Post with ID 1:", post_data.title, post_data.category)  # Print the title and category of the post with ID 1
            post_data.title = "The Godfather"
            post_data.save()  # Save the updated post data

        # Filter posts based on category ID
        filtered_posts = Post.filter(category=category.id, order_by='-create_time')  # Retrieve all posts associated with the specified category ID
        print("Filtered Posts:", [(post.title, post.category) for post in filtered_posts])  # Print posts filtered by category

        # Update an existing post
        Post.update(1, title='Updated Godfather')  # Update the title of the post with ID 1 to 'Updated Godfather'

        # Read all posts after updating
        updated_posts = Post.all()  # Retrieve all posts from the database after the update
        print("Updated Posts:", [(post.title, post.category) for post in updated_posts])  # Print all posts with updated details

        # Delete a post
        Post.delete(1)  # Delete the post with ID 1

        # Read all posts after deletion
        final_posts = Post.all(order_by='create_time')  # Retrieve all posts from the database after deletion
        print("Final Posts:", [(post.title, post.category) for post in final_posts])  # Print all remaining posts

    else:
        print("Category with ID 1 does not exist.")  # Print a message if the category with ID 1 does not exist
