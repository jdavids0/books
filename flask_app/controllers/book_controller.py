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

@app.route ('/books/<int:id>')
def show_book_faves(id):
    data = {
        'id' : id
    }
    book = Book.get_book_favorites(data)
    return render_template ('show_book.html', book = book)
