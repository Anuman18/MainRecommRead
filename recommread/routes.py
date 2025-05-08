import datetime
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from recommread import app, db, login_manager
from recommread.models import User, Post, Vote
from recommread.forms import LoginForm, SignupForm, PostForm, RecommendForm, SearchForm
from recommread.recommender import recommend_books, search_books

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page=page, per_page=10)
    return render_template('home.html', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = SignupForm()
    if form.validate_on_submit():
        # Check if username or email already exists
        existing_user = User.query.filter(
            (User.username == form.username.data) | 
            (User.email == form.email.data)
        ).first()
        
        if existing_user:
            if existing_user.username == form.username.data:
                flash('Username already exists', 'danger')
            else:
                flash('Email already exists', 'danger')
        else:
            # Create new user
            hashed_password = generate_password_hash(form.password.data)
            new_user = User(
                username=form.username.data,
                email=form.email.data,
                password_hash=hashed_password
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
    
    return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            user_id=current_user.id,
            timestamp=datetime.datetime.utcnow()
        )
        db.session.add(new_post)
        db.session.commit()
        flash('Your story has been posted!', 'success')
        return redirect(url_for('index'))
    
    return render_template('post.html', form=form)

@app.route('/recommend', methods=['GET', 'POST'])
@login_required
def recommend():
    form = RecommendForm()
    recommendations = []
    
    if form.validate_on_submit():
        # Get the books from the form and pass to recommender
        read_books = [book.strip() for book in form.books.data.split(',')]
        recommendations = recommend_books(read_books)
    
    return render_template('recommend.html', form=form, recommendations=recommendations)

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    results = []
    
    if form.validate_on_submit() or request.args.get('query'):
        query = form.query.data or request.args.get('query', '')
        search_type = form.search_type.data or request.args.get('search_type', 'title')
        results = search_books(query, search_type)
        form.query.data = query
        form.search_type.data = search_type
    
    return render_template('search.html', form=form, results=results)

@app.route('/vote/<int:post_id>/<action>')
@login_required
def vote(post_id, action):
    post = Post.query.get_or_404(post_id)
    
    # Check if user has already voted
    existing_vote = Vote.query.filter_by(
        user_id=current_user.id, 
        post_id=post_id
    ).first()
    
    if action == 'upvote':
        if existing_vote:
            if existing_vote.value == 1:
                # Remove vote if already upvoted
                db.session.delete(existing_vote)
            else:
                # Change downvote to upvote
                existing_vote.value = 1
        else:
            # Create new upvote
            vote = Vote(user_id=current_user.id, post_id=post_id, value=1)
            db.session.add(vote)
    
    elif action == 'downvote':
        if existing_vote:
            if existing_vote.value == -1:
                # Remove vote if already downvoted
                db.session.delete(existing_vote)
            else:
                # Change upvote to downvote
                existing_vote.value = -1
        else:
            # Create new downvote
            vote = Vote(user_id=current_user.id, post_id=post_id, value=-1)
            db.session.add(vote)
    
    db.session.commit()
    
    # Return to previous page
    return redirect(request.referrer or url_for('index'))