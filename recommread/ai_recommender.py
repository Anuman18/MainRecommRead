import os
import json
from openai import OpenAI

# The newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
MODEL = "gpt-4o"

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Sample book database with popular books across genres
# This would ideally be replaced with a more comprehensive database or API
SAMPLE_BOOKS = [
    {
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "genre": ["Literary Fiction", "Coming-of-Age", "Historical Fiction"],
        "age_range": ["Young Adult", "Adult"],
        "themes": ["Racial Injustice", "Loss of Innocence", "Moral Growth", "Empathy"],
        "year": 1960,
        "description": "A powerful story about racial injustice and moral growth, told through the eyes of a young girl in the American South."
    },
    {
        "title": "1984",
        "author": "George Orwell",
        "genre": ["Dystopian", "Science Fiction", "Political Fiction"],
        "age_range": ["Young Adult", "Adult"],
        "themes": ["Totalitarianism", "Surveillance", "Mind Control", "Rebellion"],
        "year": 1949,
        "description": "A chilling portrayal of a totalitarian regime where the government controls every aspect of people's lives, including their thoughts."
    },
    {
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "genre": ["Fantasy", "Adventure"],
        "age_range": ["Middle Grade", "Young Adult", "Adult"],
        "themes": ["Heroism", "Journey", "Personal Growth", "Greed"],
        "year": 1937,
        "description": "A fantasy adventure that follows Bilbo Baggins as he journeys with dwarves to reclaim their mountain home from a dragon."
    },
    {
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "genre": ["Romance", "Classic Literature"],
        "age_range": ["Young Adult", "Adult"],
        "themes": ["Love", "Social Class", "Prejudice", "Personal Growth"],
        "year": 1813,
        "description": "A witty exploration of the societal expectations, manners, and marriage in early 19th-century England."
    },
    {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "genre": ["Literary Fiction", "Historical Fiction"],
        "age_range": ["Young Adult", "Adult"],
        "themes": ["American Dream", "Wealth", "Love", "Illusion"],
        "year": 1925,
        "description": "A portrait of the Jazz Age in America, exploring themes of wealth, love, and the corrupted American Dream."
    },
    {
        "title": "Harry Potter and the Sorcerer's Stone",
        "author": "J.K. Rowling",
        "genre": ["Fantasy", "Young Adult"],
        "age_range": ["Middle Grade", "Young Adult", "Adult"],
        "themes": ["Friendship", "Courage", "Good vs. Evil", "Coming-of-Age"],
        "year": 1997,
        "description": "The first book in the beloved series follows Harry Potter as he discovers he is a wizard and begins his magical education."
    },
    {
        "title": "The Hunger Games",
        "author": "Suzanne Collins",
        "genre": ["Dystopian", "Young Adult", "Science Fiction"],
        "age_range": ["Young Adult", "Adult"],
        "themes": ["Survival", "Sacrifice", "Rebellion", "Media Influence"],
        "year": 2008,
        "description": "In a dystopian future, Katniss Everdeen volunteers to take her sister's place in a televised fight-to-the-death competition."
    },
    {
        "title": "The Road",
        "author": "Cormac McCarthy",
        "genre": ["Post-Apocalyptic", "Literary Fiction"],
        "age_range": ["Adult"],
        "themes": ["Survival", "Father-Son Relationship", "Hope", "Morality"],
        "year": 2006,
        "description": "A father and son journey through a post-apocalyptic world, facing starvation, cold, and dangerous groups of survivors."
    },
    {
        "title": "The Alchemist",
        "author": "Paulo Coelho",
        "genre": ["Fiction", "Fantasy", "Philosophical"],
        "age_range": ["Young Adult", "Adult"],
        "themes": ["Personal Legend", "Dreams", "Fate", "Spiritual Journey"],
        "year": 1988,
        "description": "A philosophical tale about a shepherd boy who dreams of finding a worldly treasure and embarks on a journey of self-discovery."
    },
    {
        "title": "Dune",
        "author": "Frank Herbert",
        "genre": ["Science Fiction", "Space Opera"],
        "age_range": ["Young Adult", "Adult"],
        "themes": ["Politics", "Religion", "Ecology", "Human Evolution"],
        "year": 1965,
        "description": "An epic science fiction tale set on the desert planet Arrakis, dealing with politics, religion, and ecology."
    },
    {
        "title": "The Catcher in the Rye",
        "author": "J.D. Salinger",
        "genre": ["Coming-of-Age", "Literary Fiction"],
        "age_range": ["Young Adult", "Adult"],
        "themes": ["Alienation", "Identity", "Loss of Innocence", "Rebellion"],
        "year": 1951,
        "description": "A teenage boy's experiences in New York City after being expelled from prep school, dealing with themes of adolescent angst and alienation."
    },
    {
        "title": "Where the Crawdads Sing",
        "author": "Delia Owens",
        "genre": ["Mystery", "Literary Fiction", "Coming-of-Age"],
        "age_range": ["Adult"],
        "themes": ["Isolation", "Survival", "Love", "Prejudice"],
        "year": 2018,
        "description": "The story of Kya Clark, the 'Marsh Girl' who grows up isolated in the marshes of North Carolina, later becoming the prime suspect in a murder."
    },
    {
        "title": "The Silent Patient",
        "author": "Alex Michaelides",
        "genre": ["Psychological Thriller", "Mystery"],
        "age_range": ["Adult"],
        "themes": ["Psychological Trauma", "Truth", "Therapy", "Deception"],
        "year": 2019,
        "description": "A psychological thriller about a woman who stops speaking after allegedly murdering her husband, and the therapist determined to unravel her mystery."
    },
    {
        "title": "The Name of the Wind",
        "author": "Patrick Rothfuss",
        "genre": ["Fantasy", "Epic"],
        "age_range": ["Young Adult", "Adult"],
        "themes": ["Education", "Power", "Love", "Music"],
        "year": 2007,
        "description": "The first day of the autobiography of Kvothe, an adventurer and famous musician, as he recounts his transformation from a talented young boy to the most notorious wizard his world has ever seen."
    },
    {
        "title": "Normal People",
        "author": "Sally Rooney",
        "genre": ["Literary Fiction", "Romance", "Contemporary"],
        "age_range": ["Young Adult", "Adult"],
        "themes": ["Social Class", "Love", "Communication", "Identity"],
        "year": 2018,
        "description": "A modern love story following the relationship between Connell and Marianne from their school days in a small Irish town to their undergraduate years at Trinity College."
    },
    {
        "title": "The Martian",
        "author": "Andy Weir",
        "genre": ["Science Fiction", "Adventure"],
        "age_range": ["Young Adult", "Adult"],
        "themes": ["Survival", "Isolation", "Human Ingenuity", "Space Exploration"],
        "year": 2011,
        "description": "An astronaut is stranded on Mars after his team assumes he's dead, and he must use his scientific know-how to survive until rescue can arrive."
    },
    {
        "title": "Educated",
        "author": "Tara Westover",
        "genre": ["Memoir", "Autobiography"],
        "age_range": ["Adult"],
        "themes": ["Education", "Family", "Self-Discovery", "Resilience"],
        "year": 2018,
        "description": "A memoir about growing up in a survivalist family in Idaho and the author's journey to education, culminating in earning a PhD from Cambridge University."
    },
    {
        "title": "Little Women",
        "author": "Louisa May Alcott",
        "genre": ["Classic Literature", "Coming-of-Age"],
        "age_range": ["Middle Grade", "Young Adult", "Adult"],
        "themes": ["Family", "Gender Roles", "Love", "Independence"],
        "year": 1868,
        "description": "The story of the four March sisters—Meg, Jo, Beth, and Amy—and their passage from childhood to womanhood during the American Civil War."
    },
    {
        "title": "The Three-Body Problem",
        "author": "Liu Cixin",
        "genre": ["Science Fiction", "Hard Science Fiction"],
        "age_range": ["Adult"],
        "themes": ["First Contact", "Physics", "Cultural Revolution", "Human Extinction"],
        "year": 2008,
        "description": "Set against the backdrop of China's Cultural Revolution, a secret military project sends signals into space to establish contact with aliens, leading to Earth's impending invasion."
    },
    {
        "title": "The Night Circus",
        "author": "Erin Morgenstern",
        "genre": ["Fantasy", "Historical Fiction", "Romance"],
        "age_range": ["Young Adult", "Adult"],
        "themes": ["Competition", "Love", "Fate", "Magic"],
        "year": 2011,
        "description": "A competition between two young magicians set in a mysterious circus that only appears at night, as they fall in love despite being pitted against each other."
    }
]

def get_advanced_recommendations(user_preferences):
    """
    Generate book recommendations using OpenAI's GPT-4o based on user preferences
    
    Args:
        user_preferences (dict): Contains user's age_range, favorite_genres, and previously read books
        
    Returns:
        list: A list of recommended books with titles, authors, and descriptions
    """
    age_range = user_preferences.get('age_range', 'Adult')
    favorite_genres = user_preferences.get('favorite_genres', [])
    read_books = user_preferences.get('read_books', [])
    
    # Convert read_books to a simple list if it's a string
    if isinstance(read_books, str):
        read_books = [book.strip() for book in read_books.split(',')]
    
    # Prepare the prompt for OpenAI
    system_prompt = """
    You are a sophisticated book recommendation system with expertise in literature across all genres and age groups.
    Based on the user's age range, preferred genres, and previously read books, recommend 5 books they might enjoy.
    
    For each recommendation, provide:
    1. Title
    2. Author
    3. A brief, compelling description of why they might enjoy it based on their preferences
    
    Format your response as a JSON array of objects with the fields: title, author, and description.
    Do not include any explanatory text outside the JSON structure.
    """
    
    user_prompt = f"""
    Please recommend books for a reader with these preferences:
    
    Age Range: {age_range}
    Favorite Genres: {', '.join(favorite_genres) if favorite_genres else 'Open to all genres'}
    Previously Read Books: {', '.join(read_books) if read_books else 'None specified'}
    
    Make sure to provide diverse recommendations that match their preferences but also introduce them to potentially new interests.
    Return only a valid JSON array.
    """
    
    try:
        # Call the OpenAI API
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        # Parse the response
        recommendation_text = response.choices[0].message.content
        recommendations = json.loads(recommendation_text)
        
        # If the response is not in the expected format, we need to fix it
        if not isinstance(recommendations, dict) or 'recommendations' not in recommendations:
            if isinstance(recommendations, list):
                return recommendations
            else:
                # Try to find any array in the response
                for key, value in recommendations.items():
                    if isinstance(value, list):
                        return value
                
                # Fallback to a simple structure
                return [{"title": "Unable to parse recommendations", "author": "", "description": "Please try again with different preferences."}]
        
        return recommendations['recommendations']
    
    except Exception as e:
        print(f"Error in AI recommendation: {str(e)}")
        # Fallback to a simple recommendation system if OpenAI fails
        return fallback_recommendations(user_preferences)

def fallback_recommendations(user_preferences):
    """Fallback recommendation system when the AI service is unavailable"""
    age_range = user_preferences.get('age_range', 'Adult')
    favorite_genres = user_preferences.get('favorite_genres', [])
    read_books = user_preferences.get('read_books', [])
    
    # Convert read_books to a simple list if it's a string
    if isinstance(read_books, str):
        read_books = [book.strip() for book in read_books.split(',')]
    
    # Filter books by age range
    suitable_books = [book for book in SAMPLE_BOOKS 
                     if age_range in book['age_range']]
    
    # Filter by genre if genres are specified
    if favorite_genres:
        genre_matches = []
        for book in suitable_books:
            for genre in book['genre']:
                if any(fg.lower() in genre.lower() for fg in favorite_genres):
                    genre_matches.append(book)
                    break
        
        if genre_matches:
            suitable_books = genre_matches
    
    # Remove books already read
    suitable_books = [book for book in suitable_books 
                     if book['title'] not in read_books]
    
    # Sort by relevance (simplified approach)
    # In a real system, you would use a more sophisticated algorithm
    if favorite_genres:
        def genre_match_score(book):
            return sum(1 for genre in book['genre'] 
                      if any(fg.lower() in genre.lower() for fg in favorite_genres))
        
        suitable_books.sort(key=genre_match_score, reverse=True)
    
    # Take top 5 recommendations or all if less than 5
    recommendations = suitable_books[:5]
    
    # Format the output to match the AI recommendation format
    formatted_recommendations = []
    for book in recommendations:
        formatted_recommendations.append({
            "title": book['title'],
            "author": book['author'],
            "description": book['description']
        })
    
    return formatted_recommendations

def get_book_cover_url(title, author):
    """
    Generate a URL for a book cover image using Open Library API
    
    Args:
        title (str): Book title
        author (str): Book author
        
    Returns:
        str: URL to the book cover image
    """
    # Replace spaces with + for URL formatting
    title_formatted = title.replace(' ', '+')
    author_formatted = author.replace(' ', '+')
    
    # Open Library ID format for cover images
    cover_url = f"https://covers.openlibrary.org/b/title/{title_formatted}-M.jpg"
    
    return cover_url