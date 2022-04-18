from flask_app import app

from flask import render_template, request, redirect

from flask_app.models.author import Author
from flask_app.models.book import Book

@app.route ('/')
def index():
    return redirect ('/authors')

@app.route ('/authors')
def show_all_authors():
    authors = Author.show_all_authors()
    return render_template ('authors.html', authors = authors)

@app.route ('/create/author', methods=['POST'])
def create_author():

    data = {
        'name' : request.form['name'],
        'created_at' : 'NOW()',
        'updated_at' : 'NOW()'
    }

    Author.create_author(data)

    return redirect ('/authors')

@app.route ('/authors/<int:id>')
def show_author_faves(id):
    data = {
        'id' : id
    }
    author = Author.get_author_favorites(data)
    books = Book.unfavorited_books(data)
    return render_template('show_author.html', books = books, author = author)

@app.route ('/add/author/favorite', methods=['POST'])
def add_author_favorite():

    return redirect ('/author/<int:id>')