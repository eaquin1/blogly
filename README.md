# blogly

This is a multi-unit exercise to practice SQLAlchemy with relationships. Each part corresponds to a unit so make sure that you complete one part and then go onto the next unit.

In it, you’ll build “Blogly”, a blogging application.

First, create a User model for SQLAlchemy. Put this in a models.py file.

It should have the following columns:

- id, an autoincrementing integer number that is the primary key
- first_name and last_name
- image_url for profile images

Make good choices about whether things should be required, have defaults, and so on.

## Create Flask App

Next, create a skeleton Flask app. You can pattern match from the lecture demo.

It should be able to import the User model, and create the tables using SQLAlchemy. Make sure you have the FlaskDebugToolbar installed — it’s especially helpful when using SQLAlchemy.

## Make a Base Template

Add a base template with slots for the page title and content. Your other templates should use this.

You can use Bootstrap for this project, but don’t spend a lot of time worrying about styling — this is not a goal of this exercise.
