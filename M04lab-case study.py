#case study.py
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'  # Replace with your database URI
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100))
    author = db.Column(db.String(100))
    publisher = db.Column(db.String(100))

    def __init__(self, book_name, author, publisher):
        self.book_name = book_name
        self.author = author
        self.publisher = publisher

# Create a new book
@app.route('/books', methods=['POST'])
def create_book():
    book_name = request.json['book_name']
    author = request.json['author']
    publisher = request.json['publisher']
    new_book = Book(book_name=book_name, author=author, publisher=publisher)
    db.session.add(new_book)
    db.session.commit()
    return {'message': 'Book created successfully'}

# Get all books
@app.route('/books', methods=['GET'])
def get_all_books():
    books = Book.query.all()
    return [{'id': book.id, 'book_name': book.book_name, 'author': book.author, 'publisher': book.publisher} for book in books]

# Get a book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if book:
        return {'id': book.id, 'book_name': book.book_name, 'author': book.author, 'publisher': book.publisher}
    else:
        return {'message': 'Book not found'}, 404

# Update a book by ID
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get(book_id)
    if book:
        book.book_name = request.json.get('book_name', book.book_name)
        book.author = request.json.get('author', book.author)
        book.publisher = request.json.get('publisher', book.publisher)
        db.session.commit()
        return {'message': 'Book updated successfully'}
    else:
        return {'message': 'Book not found'}, 404

# Delete a book by ID
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return {'message': 'Book deleted successfully'}
    else:
        return {'message': 'Book not found'}, 404

if __name__ == '__main__':
    app.run(debug=True)