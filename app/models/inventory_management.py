# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime
# from app.models.stock_changes import StockChange

# db = SQLAlchemy()

# class InventoryManagement(db.Model):
#     __tablename__ = 'inventory_management'

#     id = db.Column(db.Integer, primary_key=True)
#     product_id = db.Column(db.Integer, db.ForeignKey('products.id'), unique=True, nullable=False)
#     current_quantity = db.Column(db.Integer, nullable=False, default=0)
#     low_stock_threshold = db.Column(db.Integer, nullable=False, default=10)
#     location = db.Column(db.String(100), nullable=True)
#     last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     product = db.relationship('Product', backref='inventory_management', uselist=False)
#     stock_changes = db.relationship('StockChange', backref='inventory_management', lazy=True, cascade="all, delete-orphan")

#     def __repr__(self):
#         return f"<InventoryManagement(product_id={self.product_id}, current_quantity={self.current_quantity}, location={self.location})>"

#     def is_low_stock(self):
#         return self.current_quantity <= self.low_stock_threshold

#     def get_stock_status(self):
#         return 'in_stock' if self.current_quantity > 0 else 'out_of_stock'

#     def update_stock(self, quantity_change, change_type):
#         new_quantity = self.current_quantity + quantity_change
#         if new_quantity < 0:
#             raise ValueError("Cannot reduce stock below 0")
#         self.current_quantity = new_quantity
#         self.last_updated = datetime.utcnow()
#         stock_change = StockChange(
#             inventory_management_id=self.id,
#             change_type=change_type,
#             change_amount=quantity_change
#         )
#         db.session.add(stock_change)
#         db.session.commit()