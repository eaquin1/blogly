from models import User, db
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

# Add new objects to session, so they'll persist
db.session.add(alda)
db.session.add(burton)
db.session.add(smith)
db.session.add(swift)
db.session.add(cures)
db.session.add(wexler)

# Commit--otherwise, this never gets saved!
db.session.commit()
