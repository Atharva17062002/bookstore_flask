from cart import db,app 
from cart.models import Cart, CartItems
import requests as http




def get_or_create_cart(user_id):
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.session.add(cart)
        db.session.commit()
    return cart

def get_book_from_inventory(book_id, authorization_header):
    url = f"http://127.0.0.1:7001/book/{book_id}"
    response = http.get(url, headers={"Authorization": authorization_header})
    return response.json()

def check_if_exists_in_inv(book_id):
    book = CartItems.query.filter_by(book_id=book_id).first()
    return book

def update_cart(cart,book_data, req_data):
    cart_item = CartItems.query.filter_by(book_id=book_data['id'],cart_id= cart.id).first()
    if not cart_item:
        cart_item = CartItems(
            book_id = book_data['id'],
            cart_id = cart.id,
            price = book_data['price'],
            quantity = req_data['quantity']
        )
        db.session.add(cart_item)
    else:
        cart_item.quantity = req_data['quantity']
    db.session.commit()
    cart.total_price = sum([item.price * item.quantity for item in cart.items])
    cart.total_quantity = sum([item.quantity for item in cart.items])
    db.session.commit() 

def delete_cart(c_id):
    cart = Cart.query.filter_by(id = c_id).first()
    if not cart:
        return False
    db.session.delete(cart)
    # db.session.commit()
    return True

def validate_quantity(book_data,quantity):
    if book_data['quantity'] < int(quantity):
        return False
    else:
        return True

def order_book(cart, token):
    cart_item = cart.items    
    for i in cart_item:
        a = get_book_from_inventory(i.book_id, token)['data']
        if(validate_quantity(a,i.quantity) == False):
            return False
    print([item.to_json() for item in cart_item])
    response = http.put(f"http://127.0.0.1:7001/api/v1/updateQuantity", headers={"Authorization": token},json = {"book_details": [item.to_json() for item in cart_item]} )
    print(response.text)
    cart.is_ordered = True
    db.session.commit()
    return True

def cancel_order(cart,token):
    cart_items = cart.items
    response = http.post("http://127.0.0.1:7001/api/v1/updateQuantity", headers={"Authorization": token},json = {"book_details": [item.to_json() for item in cart_items]} )
    cart.is_ordered = False
    db.session.commit()
    return True