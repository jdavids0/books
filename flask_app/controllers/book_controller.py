from flask_app import app

from flask import render_template, request, redirect

from flask_app.models.author import Author
from flask_app.models.book import Book


@app.route ('/books')
def show_all_books():
    books = Book.show_all_books()
    return render_template ('books.html', books = books)

@app.route ('/create/book', methods=['POST'])
def create_book():

    data = {
        'title' : request.form['title'],
        'pages' : request.form['pages'],
        'created_at' : 'NOW()',
        'updated_at' : 'NOW()'
    }

    Book.create_book(data)

    return redirect ('/books')

@app.route ('/book/<int:id>')
def show_book_faves(id):
    data = {
        'id' : id
    }
    author = Author.unfavorited_authors(data)
    book = Book.get_book_favorites(data)
    return render_template ('show_book.html', book = book, author = author)

@app.route('/add/book/favorite', methods=['POST'])
def add_book_favorite():
    data = {
        'author_id' : request.form['author_id'],
        'book_id' : request.form['book_id']
    }
    Author.add_favorite(data)
    return redirect(f"/book/{request.form['book_id']}")
