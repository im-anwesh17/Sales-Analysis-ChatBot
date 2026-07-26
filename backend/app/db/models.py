from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Index, Text, Boolean
from sqlalchemy.orm import relationship
from app.db.session import Base


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=True)
    city = Column(String(50), index=True, nullable=False)
    state = Column(String(50), index=True, nullable=False)
    country = Column(String(50), default="United States")
    segment = Column(String(30), index=True, default="Consumer")  # Consumer, Corporate, Home Office
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    orders = relationship("Order", back_populates="customer", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Customer {self.first_name} {self.last_name} ({self.email})>"


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(150), nullable=False, index=True)
    category = Column(String(50), nullable=False, index=True)  # Electronics, Clothing, Home & Kitchen, Accessories
    subcategory = Column(String(50), nullable=False, index=True)
    unit_price = Column(Float, nullable=False)
    cost_price = Column(Float, nullable=False)
    sku = Column(String(50), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)

    # Relationships
    order_items = relationship("OrderItem", back_populates="product")

    def __repr__(self):
        return f"<Product {self.product_name} - ${self.unit_price}>"


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=False, index=True)
    order_date = Column(DateTime, nullable=False, index=True)
    shipping_city = Column(String(50), nullable=False)
    shipping_state = Column(String(50), nullable=False, index=True)
    shipping_country = Column(String(50), default="United States")
    status = Column(String(20), nullable=False, default="Completed", index=True)  # Completed, Pending, Cancelled, Returned
    payment_method = Column(String(30), nullable=False, default="Credit Card")
    total_amount = Column(Float, nullable=False, default=0.0)

    # Relationships
    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_order_date_status", "order_date", "status"),
    )

    def __repr__(self):
        return f"<Order #{self.order_id} - ${self.total_amount} ({self.status})>"


class OrderItem(Base):
    __tablename__ = "order_items"

    item_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Float, nullable=False)
    discount = Column(Float, nullable=False, default=0.0)  # Percentage (0.0 to 0.5)
    total_amount = Column(Float, nullable=False)

    # Relationships
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

    def __repr__(self):
        return f"<OrderItem #{self.item_id} - Order #{self.order_id} - Prod #{self.product_id}>"
