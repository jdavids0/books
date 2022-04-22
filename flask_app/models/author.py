from flask_app.config.mysqlconnection import connectToMySQL

from flask_app.models import book

db = "books_schema"

class Author:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.favorite_books = []

    @classmethod
    def show_all_authors(cls):
        query = "SELECT * FROM authors"

        results = connectToMySQL(db).query_db(query)
        print(results)
        authors = []
        for x in results:
            authors.append(cls(x))
        print(authors)
        return authors

    @classmethod
    def create_author(cls, data):

        query = "INSERT INTO authors (name, created_at, updated_at) VALUES ( %(name)s, NOW(), NOW() )"

        result = connectToMySQL(db).query_db(query, data)

        return result

    @classmethod
    def get_author_favorites(cls, data):
        query = "SELECT * FROM authors LEFT JOIN favorites ON authors.id = favorites.author_id LEFT JOIN books ON books.id = favorites.book_id WHERE authors.id = %(id)s;"

        result = connectToMySQL(db).query_db(query, data)

        author = cls(result[0])

        for row in result:
            if row['books.id'] == None:
                break

            book_data = {
                'id' : row['books.id'],
                'title' : row['title'],
                'pages' : row['pages'],
                'created_at' : row['created_at'],
                'updated_at' : row['updated_at']    
            }
            author.favorite_books.append(book.Book(book_data))

        return author

    @classmethod
    def unfavorited_authors(cls, data):
        query = "SELECT * FROM authors WHERE authors.id NOT IN (SELECT author_id FROM favorites WHERE book_id = %(id)s )"

        results = connectToMySQL(db).query_db(query, data)
        
        authors = []
        for row in results:
            authors.append(cls(row))
        
        return authors

    @classmethod
    def add_favorite(cls, data):
        query = "INSERT INTO favorites (author_id, book_id) VALUES (%(author_id)s, %(book_id)s)"
        return connectToMySQL(db).query_db(query, data)


