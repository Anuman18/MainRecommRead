from datetime import datetime
from flask_login import UserMixin
from recommread import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Profile information
    bio = db.Column(db.String(500))
    favorite_book = db.Column(db.String(100))
    favorite_author = db.Column(db.String(100))
    reading_preferences = db.Column(db.String(100))  # Stored as comma-separated values
    
    # Reading preferences
    age_range = db.Column(db.String(20), default='Adult')
    favorite_genres = db.Column(db.String(200))  # Stored as comma-separated values
    
    # Relationships
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    votes = db.relationship('Vote', backref='user', lazy='dynamic')
    
    def __repr__(self):
        return f'<User {self.username}>'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    votes = db.relationship('Vote', backref='post', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Post {self.title}>'
    
    @property
    def vote_count(self):
        return sum(vote.value for vote in self.votes)
    
    def user_vote(self, user_id):
        """Return the current user's vote for this post"""
        vote = Vote.query.filter_by(user_id=user_id, post_id=self.id).first()
        if vote:
            return vote.value
        return 0

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)  # 1 for upvote, -1 for downvote
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Add a unique constraint to prevent a user from voting multiple times on the same post
    __table_args__ = (db.UniqueConstraint('user_id', 'post_id', name='user_post_vote_uc'),)
    
    def __repr__(self):
        return f'<Vote {self.value} on Post {self.post_id} by User {self.user_id}>'
