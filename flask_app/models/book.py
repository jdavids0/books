from flask_app.config.mysqlconnection import connectToMySQL

from flask_app.models import author

db = "books_schema"

class Book:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.pages = data['pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.authors_who_favorited = []

    @classmethod
    def show_all_books(cls):
        query = "SELECT * FROM books"

        results = connectToMySQL(db).query_db(query)
        print(results)
        books = []
        for x in results:
            books.append(cls(x))
        print(books)
        return books

    @classmethod
    def create_book(cls, data):

        query = "INSERT INTO books (title, pages, created_at, updated_at) VALUES ( %(title)s, %(pages)s, NOW(), NOW() )"

        result = connectToMySQL(db).query_db(query, data)

        return result

    @classmethod
    def get_book_favorites(cls, data):
        query = "SELECT * FROM books JOIN favorites ON books.id = favorites.book_id JOIN authors ON authors.id = favorites.author_id WHERE books.id = %(id)s;"

        result = connectToMySQL(db).query_db(query, data)

        book = cls(result[0])

        for row in result:
            author_data = {
                'id' : row['authors.id'],
                'name' : row['name'],
                'created_at' : row['created_at'],
                'updated_at' : row['updated_at']    
            }
            book.authors_who_favorited.append(author.Author(author_data))
        
        return book

    @classmethod
    def unfavorited_books(cls, data):
        query = "SELECT * FROM books WHERE books.id NOT IN (SELECT book_id FROM favorites WHERE author_id = %(id)s )"

        results = connectToMySQL(db).query_db(query, data)
        # create an empty list books, loop through results of query and append each row of the table it returns as an instance of the class Book
        books = []
        for row in results:
            books.append(cls(row))
        
        return books
