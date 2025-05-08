import datetime
from werkzeug.security import generate_password_hash
from recommread import db, app
from recommread.models import User, Post, Vote

def create_sample_users():
    """Create sample users for the application"""
    users = [
        {
            'username': 'alice_reader',
            'email': 'alice@example.com',
            'password': 'password123',
            'bio': 'Avid reader of classic literature and historical fiction.'
        },
        {
            'username': 'bob_bookworm',
            'email': 'bob@example.com',
            'password': 'password123',
            'bio': 'Science fiction and fantasy enthusiast. Love exploring new worlds.'
        },
        {
            'username': 'literary_emma',
            'email': 'emma@example.com',
            'password': 'password123',
            'bio': 'Book reviewer and aspiring author. I read everything I can get my hands on!'
        }
    ]
    
    created_users = []
    for user_data in users:
        # Check if user already exists
        existing_user = User.query.filter_by(username=user_data['username']).first()
        if not existing_user:
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                password_hash=generate_password_hash(user_data['password'])
            )
            db.session.add(user)
            created_users.append(user)
    
    db.session.commit()
    return created_users

def create_sample_posts(users):
    """Create sample posts for the application"""
    posts = [
        {
            'author_index': 0,
            'title': 'Why "To Kill a Mockingbird" Remains Relevant Today',
            'content': """Harper Lee's classic novel continues to resonate with readers of all ages. The themes of racial injustice, moral growth, and compassion are unfortunately still relevant in today's society.

The character of Atticus Finch represents the moral compass we all aspire to follow - standing up for what's right, even when it's difficult. Scout's coming-of-age journey teaches us about seeing the world through others' eyes.

I recently reread this masterpiece and found new layers of meaning I had missed during my first reading in school. The prose is beautiful in its simplicity yet profound in its message. If you haven't revisited this book as an adult, I highly recommend it."""
        },
        {
            'author_index': 1,
            'title': 'Exploring Dune\'s Complex Universe',
            'content': """Frank Herbert's "Dune" is not just science fiction - it's a masterclass in world-building. The ecology, religion, politics, and sociology of Arrakis create a universe that feels completely real and lived-in.

What I appreciate most about this book is how it challenges the traditional hero's journey. Paul Atreides' transformation forces readers to question the nature of power and the consequences of messianic figures.

The attention to detail in the Fremen culture and the spice economy shows Herbert's incredible imagination and foresight. The themes of environmental conservation and resource management were ahead of their time.

What's your favorite aspect of the Dune universe? I'd love to hear other perspectives on this science fiction masterpiece."""
        },
        {
            'author_index': 2,
            'title': 'The Enduring Appeal of Jane Austen',
            'content': """Jane Austen's novels have captivated readers for centuries, and it's easy to see why. Her sharp social commentary, complex characters, and subtle humor create stories that transcend their time period.

"Pride and Prejudice" remains my favorite, with the evolution of Elizabeth and Darcy's relationship showing Austen's deep understanding of human nature. The witty dialogue and memorable supporting characters (Mr. Collins, anyone?) make every reread a delight.

What makes Austen special is her ability to work within the constraints of her society while subtly challenging its norms. Her female protagonists have agency and intelligence in a time when women had limited options.

I recommend starting with "Pride and Prejudice" if you're new to Austen, but don't miss "Persuasion" - it's a more mature work with a deeply moving second-chance romance."""
        },
        {
            'author_index': 0,
            'title': 'My Journey Through Tolkien\'s Middle-earth',
            'content': """I've just completed my annual reread of "The Lord of the Rings" trilogy, and I'm once again in awe of Tolkien's achievement. The depth of his world-building is unparalleled - from constructed languages to detailed histories spanning thousands of years.

What strikes me most about these books is how they balance epic scope with intimate character moments. The friendship between Sam and Frodo, Aragorn's reluctant leadership, and Gandalf's wisdom all feel genuine despite the fantastical setting.

The themes of courage in the face of overwhelming odds, the corruption of power, and the importance of hope resonate deeply. Tolkien's own experiences in World War I clearly influenced his portrayal of good versus evil.

If you've only seen the films, I highly recommend experiencing the books. Tolkien's prose has a lyrical quality that brings Middle-earth to life in ways even the best visual effects cannot match."""
        },
        {
            'author_index': 1,
            'title': 'Why "1984" Should Be Required Reading',
            'content': """George Orwell's "1984" is often referenced in political discussions, but nothing compares to actually reading this powerful dystopian novel. The concepts of doublethink, Newspeak, and thoughtcrime have become part of our vocabulary for good reason.

What makes this book so chilling is not just the totalitarian surveillance state, but the systematic destruction of truth itself. The Party's ability to alter history and control language demonstrates how authoritarianism attacks the very foundation of individual thought.

Winston Smith's desperate attempt to maintain his humanity in an inhuman system is both heartbreaking and compelling. His relationship with Julia shows how personal connection becomes the ultimate form of rebellion.

In an era of misinformation and privacy concerns, Orwell's warnings feel more urgent than ever. This isn't just a classic - it's a crucial lens through which to view power and truth in any society."""
        },
        {
            'author_index': 2,
            'title': 'The Hidden Depths of "The Great Gatsby"',
            'content': """F. Scott Fitzgerald's masterpiece is often reduced to its surface elements - the parties, the wealth, the tragic love story. But beneath the glittering facade of the Jazz Age lies a profound exploration of the American Dream.

Gatsby's pursuit of Daisy represents the fundamental illusion at the heart of materialism - the belief that wealth and status can recapture the past or secure love. The green light across the bay perfectly symbolizes the perpetual reaching for what remains just out of grasp.

Nick Carraway's position as both insider and observer gives readers a nuanced perspective on the moral emptiness behind the era's prosperity. His journey from admiration to disillusionment mirrors America's own complicated relationship with success.

The novel's prose is simply stunning - Fitzgerald crafts sentences that capture both the intoxication of possibility and the melancholy of its limitations. The final paragraphs rank among the most beautiful in American literature."""
        }
    ]
    
    for post_data in posts:
        # Ensure we have a valid user index
        if post_data['author_index'] < len(users):
            user = users[post_data['author_index']]
            
            # Check if post already exists
            existing_post = Post.query.filter_by(title=post_data['title'], user_id=user.id).first()
            if not existing_post:
                post = Post(
                    title=post_data['title'],
                    content=post_data['content'],
                    user_id=user.id,
                    timestamp=datetime.datetime.utcnow()
                )
                db.session.add(post)
    
    db.session.commit()

def create_sample_votes(users):
    """Create sample votes for posts"""
    # Get all posts
    posts = Post.query.all()
    
    # Create some sample voting patterns
    for i, post in enumerate(posts):
        # Each user votes on most posts, with different patterns
        for j, user in enumerate(users):
            # Skip if the user is the author of the post
            if post.user_id == user.id:
                continue
                
            # Different voting patterns based on user and post combination
            if (i + j) % 3 == 0:  # Some upvotes
                vote_value = 1
            elif (i + j) % 5 == 0:  # Some downvotes
                vote_value = -1
            else:
                continue  # No vote for this combination
            
            # Check if vote already exists
            existing_vote = Vote.query.filter_by(user_id=user.id, post_id=post.id).first()
            if not existing_vote:
                vote = Vote(
                    user_id=user.id,
                    post_id=post.id,
                    value=vote_value,
                    timestamp=datetime.datetime.utcnow()
                )
                db.session.add(vote)
    
    db.session.commit()

def seed_database():
    """Seed the database with sample data"""
    with app.app_context():
        # Create sample users
        users = create_sample_users()
        
        # If we didn't get any users back, query for existing ones
        if not users:
            users = User.query.all()
        
        # Only continue if we have users
        if users:
            # Create sample posts
            create_sample_posts(users)
            
            # Create sample votes
            create_sample_votes(users)
            
            print("Database seeded successfully!")
        else:
            print("No users available for seeding posts.")

if __name__ == "__main__":
    seed_database()