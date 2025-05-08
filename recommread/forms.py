from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, SelectField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from recommread.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), 
        Length(min=3, max=64, message='Username must be between 3 and 64 characters')
    ])
    email = StringField('Email', validators=[
        DataRequired(), 
        Email(message='Invalid email address')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Sign Up')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[
        DataRequired(),
        Length(min=5, max=100, message='Title must be between 5 and 100 characters')
    ])
    content = TextAreaField('Content', validators=[
        DataRequired(),
        Length(min=10, message='Content must be at least 10 characters')
    ])
    submit = SubmitField('Post Story')

class RecommendForm(FlaskForm):
    books = TextAreaField('Enter books you\'ve read (comma separated)', validators=[
        DataRequired(),
        Length(min=2, message='Please enter at least one book title')
    ])
    
    age_range = SelectField('Your Age Range', choices=[
        ('Middle Grade', 'Middle Grade (8-12)'),
        ('Young Adult', 'Young Adult (13-18)'),
        ('Adult', 'Adult (18+)'),
        ('All', 'All Ages')
    ], default='Adult')
    
    favorite_genres = SelectMultipleField('Favorite Genres (Select up to 3)', choices=[
        ('Literary Fiction', 'Literary Fiction'),
        ('Science Fiction', 'Science Fiction'),
        ('Fantasy', 'Fantasy'),
        ('Mystery', 'Mystery'),
        ('Thriller', 'Thriller'),
        ('Romance', 'Romance'),
        ('Historical Fiction', 'Historical Fiction'),
        ('Dystopian', 'Dystopian'),
        ('Adventure', 'Adventure'),
        ('Coming-of-Age', 'Coming-of-Age'),
        ('Memoir', 'Memoir/Biography'),
        ('Poetry', 'Poetry'),
        ('Horror', 'Horror'),
        ('Classics', 'Classics'),
        ('Contemporary', 'Contemporary Fiction'),
        ('Young Adult', 'Young Adult Fiction'),
        ('Philosophy', 'Philosophy'),
        ('Self-Help', 'Self-Help'),
        ('Non-Fiction', 'Non-Fiction')
    ])
    
    submit = SubmitField('Get AI-Powered Recommendations')

class ProfileForm(FlaskForm):
    bio = TextAreaField('Bio', validators=[
        Length(max=500, message='Bio must be less than 500 characters')
    ])
    favorite_book = StringField('Favorite Book', validators=[
        Length(max=100, message='Favorite book must be less than 100 characters')
    ])
    favorite_author = StringField('Favorite Author', validators=[
        Length(max=100, message='Favorite author must be less than 100 characters')
    ])
    reading_preferences = SelectMultipleField('Reading Preferences', choices=[
        ('paper', 'Paper Books'),
        ('ebook', 'E-Books'),
        ('audiobook', 'Audiobooks')
    ])
    submit = SubmitField('Update Profile')

class SearchForm(FlaskForm):
    query = StringField('Search', validators=[DataRequired()])
    search_type = SelectField('Search By', choices=[
        ('title', 'Title'),
        ('author', 'Author'),
        ('genre', 'Genre')
    ])
    submit = SubmitField('Search')
