"""      
        post (adding) ,  patch(updating), get , delete(both cart and cart item)
"""
from flask import request, jsonify, g
from cart.models import Cart, CartItems, db
from cart.schema import CartSchema
from app.utils import api_handler, JWT
from flask_restx import Api, Resource, fields
from app.middleware import auth_user
from settings import settings
# from app.tasks import celery_send_email
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import jwt
from cart import app
from cart.cart_utils import update_cart, get_book_from_inventory,get_or_create_cart,check_if_exists_in_inv,delete_cart,validate_quantity,order_book,cancel_order

# limiter = Limiter(get_remote_address, app=app, default_limits=["200 per day", "50 per hour"])

api = Api(app=app, 
        version='1.0', 
        title='Cart API', 
        description='A simple Cart API', 
        prefix='/api/v1',
        security='apikey', authorizations={'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'required': True }},
        doc='/docs')

@api.route('/update')
class UpdateCart(Resource):
        method_decorators = [auth_user]
        @api.expect(api.model('update', {"book_id":fields.Integer,"quantity":fields.Integer}),api.response(201, CartSchema))
        @api_handler()
        def post(self , *args , **kwargs):
                data = request.get_json()
                cart = get_or_create_cart(data["user_id"])
                get_book = get_book_from_inventory(data["book_id"],request.headers["Authorization"])
                if(validate_quantity(get_book['data'],data["quantity"])):
                        update_cart(cart, get_book['data'],data)
                        return {"message": "Cart updated", "status": 201, "data": cart.to_json }, 201
                return {"message": "Quantity is invalid", "status": 400}, 400

        @api_handler()
        def get(self,*args, **kwargs):
                cart = Cart.query.filter_by(user_id = kwargs["user_id"]).first()
                if not cart:
                        return {"message": "Cart not found", "status": 404}, 404
                cart_item = [x.to_json for x in cart.items]
                return {"message": "Cart Items fetched", "status": 200, "data": {"cart":cart.to_json,"items": cart_item}  }, 200

        @api.doc(params = {"id":"Give cart id"},responses = {201 : "Success"})
        def delete(self,*args, **kwargs):
                cart = Cart.query.filter_by(id=request.args["id"], is_ordered=False).first()
                print(cart)
                [db.session.delete(x) for x in cart.items]
                db.session.delete(cart)
                db.session.commit()
                return {"message": "Cart deleted", "status": 200, "data":{} }, 200

@api.route('/order')
class OrderCart(Resource):
        method_decorators = [auth_user]

        @api.expect(api.model('order', {"id":fields.Integer}),api.response(201, CartSchema))
        @api_handler()
        def post(self , *args , **kwargs):
                cart = Cart.query.filter_by(id=request.json["id"], user_id=request.json["user_id"], is_ordered=False).first()
                if not cart:
                        return {"message": "Cart not found", "status": 404}, 404
                if(order_book(cart, request.headers["Authorization"])):
                        return {"message": "Order placed", "status": 201, "data":{} }, 201
                else:
                        return {"message": "Order failed", "status": 500, "data":{} }, 500

        @api.expect(api.model('order', {"id":fields.Integer}),api.response(201, CartSchema))        
        @api_handler()
        def put(self,*args, **kwargs):
                cart = Cart.query.filter_by(id=request.json["id"],user_id =request.json["user_id"], is_ordered=True).first()
                if not cart:
                        return {"message": "Cart not found", "status": 404}, 404
                if(cancel_order(cart,request.headers["Authorization"])):
                        return {"message": "Order cancelled successfully", "status": 201, "data":{} }, 201
                return {"message": "Order cancellation failed", "status": 500, "data":{} }, 500
