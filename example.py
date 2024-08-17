from abarorm.orm import SQLiteModel
from abarorm.fields import CharField, DateTimeField, ForeignKey

# Database configuration
DATABASE_CONFIG = {
    'sqlite': {
        'db_name': 'example.db',  # Name of the SQLite database file
    }
}

# Define the Category model
class Category(SQLiteModel):
    table_name = 'categories'  # Name of the table in the database

    # Define the fields of the Category model
    title = CharField(max_length=200, unique=True, null=False)  # Title of the category, must be unique and not null

    def __init__(self, **kwargs):
        # Initialize the Category model with database configuration
        super().__init__(db_config=DATABASE_CONFIG['sqlite'], **kwargs)

# Define the Post model
class Post(SQLiteModel):
    table_name = 'posts'  # Name of the table in the database

    # Define the fields of the Post model
    title = CharField(max_length=100, unique=True, null=False)  # Title of the post, must be unique and not null
    create_time = DateTimeField(auto_now=True)  # Creation time of the post, automatically set to current datetime
    category = ForeignKey(to=Category)  # Foreign key referring to the Category model

    def __init__(self, **kwargs):
        # Initialize the Post model with database configuration
        super().__init__(db_config=DATABASE_CONFIG['sqlite'], **kwargs)

# Main execution block
if __name__ == "__main__":
    # Create tables in the database
    Category.create_table()  # This will create the 'categories' table
    Post.create_table()  # This will create the 'posts' table

    # Create a new category
    Category.create(title='Movies')  # Add a new category with title 'Movies'

    # Retrieve the category for use in creating a post
    category = Category.get(id=1)  # Fetch the category with ID 1
    if category:
        # Create a new post
        Post.create(title='Godfather', category=category.id)  # Add a new post with title 'Godfather' and associate it with the fetched category

        # Read all posts
        all_posts = Post.all()  # Retrieve all posts from the database
        print("All Posts:", [(post.title, post.category) for post in all_posts])  # Print all posts with their titles and associated categories

        # Use the get method to retrieve a post by ID
        post_data = Post.get(id=1)  # Fetch the post with ID 1
        if post_data:
            print("Post with ID 1:", post_data.title, post_data.category)  # Print the title and category of the post with ID 1

        # Filter posts based on category ID
        filtered_posts = Post.filter(category=category.id)  # Retrieve all posts associated with the specified category ID
        print("Filtered Posts:", [(post.title, post.category) for post in filtered_posts])  # Print posts filtered by category

        # Update an existing post
        Post.update(1, title='Updated Godfather')  # Update the title of the post with ID 1 to 'Updated Godfather'

        # Read all posts after updating
        updated_posts = Post.all()  # Retrieve all posts from the database after the update
        print("Updated Posts:", [(post.title, post.category) for post in updated_posts])  # Print all posts with updated details

        # Delete a post
        Post.delete(1)  # Delete the post with ID 1

        # Read all posts after deletion
        final_posts = Post.all()  # Retrieve all posts from the database after deletion
        print("Final Posts:", [(post.title, post.category) for post in final_posts])  # Print all remaining posts

    else:
        print("Category with ID 1 does not exist.")  # Print a message if the category with ID 1 does not exist
