
from cart import db

class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False,)


class   Cart(BaseModel):
        __tablename__ = "cart"
        total_price = db.Column(db.Float, nullable=False,default=0)
        total_quantity = db.Column(db.Integer, nullable = False, default=0)
        is_ordered = db.Column(db.Boolean, default = False)
        created_at = db.Column(db.DateTime, nullable= False, default = db.func.now())
        updated_at = db.Column(db.DateTime, nullable= False, default = db.func.now())
        user_id = db.Column(db.Integer,nullable = False)
        items = db.relationship('CartItems', back_populates='cart')

        @property
        def to_json(self):
                return {
                    'total_price': self.total_price,
                    'total_quantity': self.total_quantity,
                    'is_ordered': self.is_ordered,
                    'created_at':str(self.created_at),
                    'updated_at': str(self.updated_at)
                }


class CartItems(BaseModel):
        __tablename__ = 'cart_items'
        price = db.Column(db.Float, nullable = False , default = 0)
        quantity = db.Column(db.Integer, nullable = False, default = 0)
        book_id = db.Column(db.Integer, nullable = False)
        cart_id = db.Column(db.Integer,db.ForeignKey('cart.id', ondelete="CASCADE"))
        cart = db.relationship('Cart',back_populates="items")

        @property
        def to_json(self):
                return {
                    'id': self.id,
                    'price': self.price,
                    'quantity': self.quantity,
                    'book_id': self.book_id,
                    'cart_id': self.cart_id,
                }
