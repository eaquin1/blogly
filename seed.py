from models import User, db, Post
from app import app

#Create all tables
db.drop_all()
db.create_all()

# If the table isn't empty, empty it
User.query.delete()

#Add users
alda = User(first_name="Alan", last_name="Alda", image_url="https://images.unsplash.com/photo-1587224702711-315d3c7f296d")
burton = User(first_name="Joel", last_name="Burton", image_url="https://images.unsplash.com/photo-1577904624593-bf2e2692efce")
smith = User(first_name="Jane", last_name="Smith", image_url="https://images.unsplash.com/photo-1585393311457-f99f89ae7004")
swift = User(first_name="Gail", last_name="Swift", image_url="https://images.unsplash.com/photo-1585393313732-03777bb1f461")
cures = User(first_name="Jimmy", last_name="Cures", image_url="https://images.unsplash.com/photo-1587160046330-8efc5abe41fa")
wexler = User(first_name="Kim", last_name="Wexler", image_url="https://images.unsplash.com/photo-1585393313732-03777bb1f461")

#Add posts
cats = Post(title="Cats", content="Adoptable cats listed here", user_id = 1)
dogs = Post(title="Dogs", content="Adoptable dogs listed here", user_id= 1)
shrimp = Post(title="Shrimp", content="Adoptable shrimp listed here", user_id = 2)
fish = Post(title="Fish", content="Adoptable fish listed here", user_id = 6)
hamster = Post(title="Hamster", content="Adoptable hamsters listed here", user_id = 4)
chickens = Post(title="Chickens", content="Adoptable chickens listed here", user_id = 3)


# Add new objects to session, so they'll persist
db.session.add_all([alda, burton, smith, swift, cures, wexler])

db.session.add_all([cats, dogs, shrimp, fish, hamster, chickens])

# Commit--otherwise, this never gets saved!
db.session.commit()
