from flask import request, jsonify, g
from books.models import Book, app, db
from books.schema import BookSchema
from app.utils import api_handler, JWT
from flask_restx import Api, Resource, fields
from app.middleware import auth_user
from settings import settings
# from app.tasks import celery_send_email
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import jwt

limiter = Limiter(get_remote_address, app=app, default_limits=["200 per day", "50 per hour"])

api = Api(app=app, 
        version='1.0', 
        title='Books API', 
        description='A simple Books API', 
        prefix='/api/v1',
         security='apikey', authorizations={'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'required': True }},
        doc='/docs')


@api.route('/books')
class BooksAPI(Resource):
    """Resource for books."""

    method_decorators = [auth_user]

    @api.expect(api.model('Add Book',{'title':fields.String(), 
                                    'author':fields.String(), 
                                    'price':fields.Integer(), 
                                    'quantity':fields.Integer()}))
    @api_handler()
    @limiter.limit("5 per minute")
    def post(self):
        if g.user["is_superuser"] == True:
            data = request.get_json()
            book = Book(**data)
            db.session.add(book)
            db.session.commit()
            db.session.refresh(book)
            # db.session.close()
            return {"message": "Book added successfully", "status": 200,'data':book.to_json}, 201
        return {"message": "You are not allowed to perform this operation", "status": 403}, 403

    @api_handler()
    @limiter.limit("50 per minute")
    def get(self,*args, **kwargs):
        books = Book.query.all()
        books = [book.to_json for book in books]
        if books :
            return {"message": "Books :", "status": 200,'data':books}, 200
        else:
            return {"message": "No books found", "status":404}, 404
    
    @api_handler()
    @limiter.limit("50 per minute")
    def delete(self,*args, **kwargs):
        if g.user["is_superuser"] == True:
            book_id = request.args.get('id')
            if not book_id:
                return {"message": "Please provide book id", "status": 400}, 400
            book = Book.query.filter_by(id=int(book_id),**kwargs).first()
            if book :
                db.session.delete(book)
                db.session.commit()
                db.session.close()
                return {"message": "Book deleted successfully", "status": 200,'data' : book.to_json}, 200
            else:
                return {"message": "No books found", "status":404}, 404
        else:
            return {"message": "You are not allowed to perform this operation", "status": 403}, 403
    
    @api_handler()
    @limiter.limit("50 per minute")
    def put(self,*args, **kwargs):
        # if g.user["is_superuser"] == True:
        data = request.get_json()
        book = Book.query.filter_by(id=data['id'], user_id=data['user_id']).first()
        [setattr(book, key, value) for key, value in data.items()]
        db.session.commit()
        # db.session.close()
        return {"message": "Book updated successfully", "status": 200,'data' : book.to_json}, 200
        # else:
        #     return {"message": "You are not allowed to perform this operation", "status": 403}, 403


# @api.doc(params={'book_id':'The book id'})
@app.route('/book/<int:book_id>', methods=['GET'])
@auth_user
def get_book(book_id, *args, **kwargs):
    if not book_id:
        return {'message': "Book id required", 'status': 400}, 400
    book = Book.query.get(book_id)
    return {'message': "Book data fetched", 'status': 200, 'data': book.to_json}, 200
        

@app.route('/updateQuantity')

class UpdateQuantity(Resource):

    method_decorators = [auth_user]

    @api_handler()
    def put(self,*args, **kwargs):
        data = request.get_json()
        for book in data['book_details']:
            b = Book.query.filter_by(id=book['book_id']).first()
            b.quantity -= book['quantity']
        db.session.commit()
        return {"message": "Quantity updated successfully", "status": 200}, 200
        
    @api_handler()
    def post(self,*args, **kwargs):
        data = request.get_json()
        for book in data['book_details']:
            b = Book.query.filter_by(id=book['book_id']).first()
            b.quantity += book['quantity']
        db.session.commit()
        return {"message": "Quantity updated successfully", "status": 200}, 200