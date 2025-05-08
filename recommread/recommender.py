import random
from difflib import SequenceMatcher

# Sample book data for demonstration purposes
# In a real application, this would come from a database or external API
BOOKS = [
    {"id": 1, "title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "Fiction", "description": "The story of racial injustice and the loss of innocence in the American South during the Great Depression."},
    {"id": 2, "title": "1984", "author": "George Orwell", "genre": "Dystopian", "description": "A dystopian social science fiction novel that examines the consequences of totalitarianism, mass surveillance, and repressive regimentation."},
    {"id": 3, "title": "Pride and Prejudice", "author": "Jane Austen", "genre": "Romance", "description": "The story follows the main character, Elizabeth Bennet, as she deals with issues of manners, upbringing, morality, education, and marriage."},
    {"id": 4, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "genre": "Fiction", "description": "Set in the Jazz Age, it tells the tragic story of Jay Gatsby, a self-made millionaire, and his pursuit of Daisy Buchanan."},
    {"id": 5, "title": "The Catcher in the Rye", "author": "J.D. Salinger", "genre": "Fiction", "description": "The story of Holden Caulfield, a teenager who recounts his experiences in New York City after being expelled from prep school."},
    {"id": 6, "title": "The Hobbit", "author": "J.R.R. Tolkien", "genre": "Fantasy", "description": "The adventures of hobbit Bilbo Baggins, who embarks on a quest to win a share of the treasure guarded by Smaug the dragon."},
    {"id": 7, "title": "Lord of the Rings", "author": "J.R.R. Tolkien", "genre": "Fantasy", "description": "The future of civilization rests in the fate of the One Ring, which has been lost for centuries."},
    {"id": 8, "title": "Harry Potter and the Philosopher's Stone", "author": "J.K. Rowling", "genre": "Fantasy", "description": "The story of Harry Potter, a boy who learns on his eleventh birthday that he is the orphaned son of two powerful wizards and possesses unique magical powers."},
    {"id": 9, "title": "The Da Vinci Code", "author": "Dan Brown", "genre": "Mystery", "description": "While in Paris, Harvard symbologist Robert Langdon is awakened by a phone call in the dead of the night."},
    {"id": 10, "title": "The Alchemist", "author": "Paulo Coelho", "genre": "Fiction", "description": "A story about an Andalusian shepherd boy named Santiago who travels from his homeland in Spain to the Egyptian desert in search of a treasure."},
    {"id": 11, "title": "Crime and Punishment", "author": "Fyodor Dostoevsky", "genre": "Psychological Fiction", "description": "The story of the mental anguish and moral dilemmas of Rodion Raskolnikov, an impoverished ex-student in Saint Petersburg who formulates a plan to kill an unscrupulous pawnbroker."},
    {"id": 12, "title": "The Hitchhiker's Guide to the Galaxy", "author": "Douglas Adams", "genre": "Science Fiction", "description": "The comedic science fiction series follows the adventures of Arthur Dent, a hapless Englishman, following the destruction of Earth by the Vogons."},
    {"id": 13, "title": "Brave New World", "author": "Aldous Huxley", "genre": "Dystopian", "description": "A dystopian novel written in 1931 that anticipates developments in reproductive technology, sleep-learning, psychological manipulation, and classical conditioning."},
    {"id": 14, "title": "Dune", "author": "Frank Herbert", "genre": "Science Fiction", "description": "Set in the distant future amidst a feudal interstellar society in which various noble houses control planetary fiefs."},
    {"id": 15, "title": "The Hunger Games", "author": "Suzanne Collins", "genre": "Dystopian", "description": "In a dystopian future, the totalitarian nation of Panem is divided into 12 districts and the Capitol. Each year two young representatives from each district are selected by lottery to participate in The Hunger Games."},
    {"id": 16, "title": "Gone Girl", "author": "Gillian Flynn", "genre": "Thriller", "description": "On the day of his fifth wedding anniversary, Nick Dunne returns home to find that his wife Amy is missing."},
    {"id": 17, "title": "The Girl with the Dragon Tattoo", "author": "Stieg Larsson", "genre": "Thriller", "description": "Journalist Mikael Blomkvist is aided in his search for a woman who has been missing for forty years by Lisbeth Salander, a young computer hacker."},
    {"id": 18, "title": "The Road", "author": "Cormac McCarthy", "genre": "Post-Apocalyptic", "description": "A father and his son walk alone through a post-apocalyptic America, heading slowly for the coast."},
    {"id": 19, "title": "The Kite Runner", "author": "Khaled Hosseini", "genre": "Historical Fiction", "description": "The story of Amir, a young boy from Kabul, whose closest friend is Hassan, his father's young Hazara servant."},
    {"id": 20, "title": "The Book Thief", "author": "Markus Zusak", "genre": "Historical Fiction", "description": "The story of Liesel Meminger, a young German girl who steals books during World War II, narrated by Death."}
]

def similarity_score(a, b):
    """Calculate string similarity between two strings"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def get_book_by_title(title):
    """Find a book in our collection by title"""
    for book in BOOKS:
        if similarity_score(book['title'], title) > 0.8:
            return book
    return None

def get_similar_books(book, books, n=5):
    """Get n books most similar to the given book based on genre"""
    if not book:
        return []
        
    # Find books with the same genre but not the same book
    same_genre = [b for b in books if b['genre'] == book['genre'] and b['id'] != book['id']]
    
    # If we don't have enough books of the same genre, add some random books
    if len(same_genre) < n:
        other_books = [b for b in books if b['genre'] != book['genre'] and b['id'] != book['id']]
        same_genre.extend(random.sample(other_books, min(n - len(same_genre), len(other_books))))
    
    # Return up to n books
    return same_genre[:n]

def recommend_books(read_books, num_recommendations=5):
    """
    Simple book recommendation based on previously read books
    This is a placeholder for a more sophisticated recommendation engine
    """
    if not read_books:
        # Return some random recommendations if no books provided
        return random.sample(BOOKS, min(num_recommendations, len(BOOKS)))
    
    recommendations = []
    
    for title in read_books:
        book = get_book_by_title(title)
        if book:
            similar_books = get_similar_books(book, BOOKS)
            for similar in similar_books:
                if similar not in recommendations and similar['title'] not in read_books:
                    recommendations.append(similar)
                    if len(recommendations) >= num_recommendations:
                        break
    
    # If we couldn't find enough recommendations based on similarity, add random ones
    if len(recommendations) < num_recommendations:
        available_books = [b for b in BOOKS if b['title'] not in read_books and b not in recommendations]
        recommendations.extend(random.sample(available_books, min(num_recommendations - len(recommendations), len(available_books))))
    
    return recommendations[:num_recommendations]

def search_books(query, search_type='title'):
    """
    Search books by title or author
    """
    results = []
    
    if not query:
        return results
    
    query = query.lower()
    
    for book in BOOKS:
        if search_type == 'title' and query in book['title'].lower():
            results.append(book)
        elif search_type == 'author' and query in book['author'].lower():
            results.append(book)
    
    # Sort results by relevance (how closely the query matches the title/author)
    if search_type == 'title':
        results.sort(key=lambda x: similarity_score(query, x['title']), reverse=True)
    else:
        results.sort(key=lambda x: similarity_score(query, x['author']), reverse=True)
    
    return results
