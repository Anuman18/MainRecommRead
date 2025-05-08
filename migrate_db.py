import os
import psycopg2
from psycopg2 import sql
from urllib.parse import urlparse

def apply_migrations():
    """Apply database migrations to add new columns to the User table"""
    # Get database connection info from environment variable
    db_url = os.environ.get("DATABASE_URL")
    
    if not db_url:
        print("ERROR: DATABASE_URL environment variable not set")
        return
    
    # Parse the DATABASE_URL to get connection parameters
    url = urlparse(db_url)
    
    # Connect to the database
    conn = psycopg2.connect(
        dbname=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    
    # Set autocommit to True to execute the ALTER TABLE statements
    conn.autocommit = True
    
    try:
        with conn.cursor() as cursor:
            print("Applying database migrations...")
            
            # Add new columns one by one to better handle errors
            migrations = [
                "ALTER TABLE \"user\" ADD COLUMN IF NOT EXISTS bio VARCHAR(500)",
                "ALTER TABLE \"user\" ADD COLUMN IF NOT EXISTS favorite_book VARCHAR(100)",
                "ALTER TABLE \"user\" ADD COLUMN IF NOT EXISTS favorite_author VARCHAR(100)",
                "ALTER TABLE \"user\" ADD COLUMN IF NOT EXISTS reading_preferences VARCHAR(100)",
                "ALTER TABLE \"user\" ADD COLUMN IF NOT EXISTS age_range VARCHAR(20) DEFAULT 'Adult'",
                "ALTER TABLE \"user\" ADD COLUMN IF NOT EXISTS favorite_genres VARCHAR(200)"
            ]
            
            for migration in migrations:
                try:
                    cursor.execute(migration)
                    print(f"Executed: {migration}")
                except Exception as e:
                    print(f"Error executing: {migration}")
                    print(f"Error: {str(e)}")
            
            print("Database migration completed.")
    
    except Exception as e:
        print(f"Migration error: {str(e)}")
    finally:
        conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    apply_migrations()