# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime

# db = SQLAlchemy()

# class StockChange(db.Model):
#     __tablename__ = 'stock_changes'

#     # Table indexes for performance
#     __table_args__ = (
#         db.Index('ix_stock_changes_inventory_management_id', 'inventory_management_id'),
#         db.Index('ix_stock_changes_created_at', 'created_at'),
#     )

#     id = db.Column(db.Integer, primary_key=True)
#     inventory_management_id = db.Column(db.Integer, db.ForeignKey('inventory_management.id'), nullable=False)
#     change_type = db.Column(db.String(50), nullable=False)  # 'stock_in' or 'stock_out'
#     change_amount = db.Column(db.Integer, nullable=False)
#     notes = db.Column(db.Text, nullable=True)  # Optional notes for the stock change
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

#     # Relationship (already defined in InventoryManagement, but explicitly shown here for clarity)
#     inventory_management = db.relationship('InventoryManagement', backref='stock_changes')

#     def __init__(self, inventory_management_id, change_type, change_amount, notes=None):
#         """Initialize a StockChange with validation."""
#         if change_type not in ['stock_in', 'stock_out']:
#             raise ValueError("change_type must be 'stock_in' or 'stock_out'")
#         self.inventory_management_id = inventory_management_id
#         self.change_type = change_type
#         self.change_amount = change_amount
#         self.notes = notes

#     def __repr__(self):
#         return f"<StockChange(inventory_management_id={self.inventory_management_id}, change_type={self.change_type}, change_amount={self.change_amount})>"

#     def get_direction(self):
#         """Returns the direction of the stock change ('increase' or 'decrease')."""
#         return 'increase' if self.change_type == 'stock_in' else 'decrease'