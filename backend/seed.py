import random
from datetime import datetime, timedelta
from faker import Faker
from sqlalchemy.orm import Session

from app.db.session import SessionLocal, engine, Base
from app.db.models import Customer, Product, Order, OrderItem
from app.core.logging import logger

fake = Faker()
Faker.seed(42)
random.seed(42)

# Sample Master Product Catalog
PRODUCTS_CATALOG = [
    # Electronics
    ("MacBook Pro 16-inch", "Electronics", "Laptops", 2499.00, 1850.00, "ELEC-MBP-16"),
    ("Dell XPS 15 Laptop", "Electronics", "Laptops", 1799.00, 1300.00, "ELEC-XPS-15"),
    ("Lenovo ThinkPad X1", "Electronics", "Laptops", 1450.00, 1050.00, "ELEC-TP-X1"),
    ("iPhone 15 Pro Max", "Electronics", "Smartphones", 1199.00, 850.00, "ELEC-IP15-PM"),
    ("Samsung Galaxy S24 Ultra", "Electronics", "Smartphones", 1299.00, 900.00, "ELEC-S24-ULT"),
    ("Sony WH-1000XM5 Headphones", "Electronics", "Audio", 399.00, 240.00, "ELEC-SONY-XM5"),
    ("AirPods Pro 2nd Gen", "Electronics", "Audio", 249.00, 160.00, "ELEC-APP-2"),
    ("LG UltraGear 32-inch 4K Monitor", "Electronics", "Monitors", 699.00, 480.00, "ELEC-LG-324K"),
    ("Apple Watch Series 9", "Electronics", "Wearables", 429.00, 290.00, "ELEC-AW-S9"),
    ("PlayStation 5 Console", "Electronics", "Gaming", 499.00, 390.00, "ELEC-PS5-CON"),
    ("Bose SoundLink Speaker", "Electronics", "Audio", 149.00, 90.00, "ELEC-BOSE-SL"),
    ("Anker 100W USB-C Dock", "Electronics", "Accessories", 89.99, 45.00, "ELEC-ANK-100W"),

    # Clothing
    ("Italian Leather Jacket", "Clothing", "Outerwear", 349.00, 180.00, "CLTH-LTHR-JKT"),
    ("Premium Wool Trench Coat", "Clothing", "Outerwear", 280.00, 140.00, "CLTH-WOOL-TRN"),
    ("Slim Fit Selvedge Denim", "Clothing", "Pants", 120.00, 55.00, "CLTH-SLM-DEN"),
    ("Heavyweight Fleece Hoodie", "Clothing", "Tops", 75.00, 30.00, "CLTH-FLC-HDD"),
    ("Nike Air Zoom Running Shoes", "Clothing", "Footwear", 140.00, 75.00, "CLTH-NK-RUN"),
    ("Adidas Ultraboost Sneakers", "Clothing", "Footwear", 180.00, 95.00, "CLTH-ADI-ULT"),
    ("Tailored Executive Blazer", "Clothing", "Suits", 299.00, 130.00, "CLTH-EXE-BLZ"),
    ("Organic Cotton Graphic Tee", "Clothing", "Tops", 35.00, 12.00, "CLTH-ORG-TEE"),
    ("Merino Wool Sweater", "Clothing", "Tops", 110.00, 48.00, "CLTH-MRN-SWT"),
    ("Chino Casual Shorts", "Clothing", "Pants", 49.99, 20.00, "CLTH-CHN-SHRT"),

    # Home & Kitchen
    ("Breville Barista Touch Espresso", "Home & Kitchen", "Appliances", 999.95, 650.00, "HOME-BREV-ESP"),
    ("Ninja Air Fryer Max XL", "Home & Kitchen", "Appliances", 169.99, 95.00, "HOME-NINJ-AF"),
    ("iRobot Roomba j7+ Vacuum", "Home & Kitchen", "Appliances", 799.00, 490.00, "HOME-RMB-J7"),
    ("Vitamix A3500 Smart Blender", "Home & Kitchen", "Appliances", 649.95, 410.00, "HOME-VITA-A35"),
    ("All-Clad 10-Piece Cookware Set", "Home & Kitchen", "Cookware", 799.00, 450.00, "HOME-ALL-10PC"),
    ("Nest Learning Thermostat 4th Gen", "Home & Kitchen", "Smart Home", 249.00, 165.00, "HOME-NST-THM"),
    ("Jarvis Electric Standing Desk", "Home & Kitchen", "Furniture", 629.00, 380.00, "HOME-JARV-DSK"),
    ("Herman Miller Aeron Ergonomic Chair", "Home & Kitchen", "Furniture", 1295.00, 820.00, "HOME-HM-AERON"),
    ("Dyson V15 Cordless Vacuum", "Home & Kitchen", "Appliances", 749.99, 480.00, "HOME-DYS-V15"),

    # Accessories
    ("Bellroy Minimalist Leather Wallet", "Accessories", "Wallets", 79.00, 32.00, "ACC-BELL-WLT"),
    ("Ray-Ban Wayfarer Sunglasses", "Accessories", "Eyewear", 163.00, 75.00, "ACC-RAY-WAY"),
    ("Peak Design Everyday Backpack 20L", "Accessories", "Bags", 279.95, 150.00, "ACC-PD-BP20"),
    ("Nomatic Travel Duffel Bag 40L", "Accessories", "Bags", 289.00, 145.00, "ACC-NOM-DUF"),
    ("Keychron Q1 Mechanical Keyboard", "Accessories", "Computer Tech", 199.00, 105.00, "ACC-KEY-Q1"),
    ("Logitech MX Master 3S Mouse", "Accessories", "Computer Tech", 99.99, 52.00, "ACC-LOG-MX3S"),
    ("Garmin Index S2 Smart Scale", "Accessories", "Fitness Tech", 149.99, 85.00, "ACC-GAR-S2")
]

CITIES_AND_STATES = [
    ("New York", "NY"), ("Los Angeles", "CA"), ("Chicago", "IL"),
    ("Houston", "TX"), ("Phoenix", "AZ"), ("Philadelphia", "PA"),
    ("San Antonio", "TX"), ("San Diego", "CA"), ("Dallas", "TX"),
    ("Austin", "TX"), ("San Jose", "CA"), ("Seattle", "WA"),
    ("San Francisco", "CA"), ("Denver", "CO"), ("Miami", "FL"),
    ("Atlanta", "GA"), ("Boston", "MA"), ("Chicago", "IL")
]

CUSTOMER_SEGMENTS = ["Consumer", "Corporate", "Home Office"]
ORDER_STATUSES = ["Completed", "Completed", "Completed", "Completed", "Pending", "Returned", "Cancelled"]
PAYMENT_METHODS = ["Credit Card", "Credit Card", "PayPal", "Bank Transfer", "UPI"]


def seed_database(db: Session):
    logger.info("Re-creating database tables...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    logger.info("Seeding products catalog...")
    products = []
    for name, cat, subcat, price, cost, sku in PRODUCTS_CATALOG:
        prod = Product(
            product_name=name,
            category=cat,
            subcategory=subcat,
            unit_price=price,
            cost_price=cost,
            sku=sku,
            is_active=True
        )
        db.add(prod)
        products.append(prod)
    db.commit()
    logger.info(f"Seeded {len(products)} products.")

    logger.info("Seeding customers...")
    customers = []
    start_customer_date = datetime(2023, 1, 1)
    for _ in range(350):
        city, state = random.choice(CITIES_AND_STATES)
        c_date = start_customer_date + timedelta(days=random.randint(0, 500))
        cust = Customer(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.unique.email(),
            phone=fake.phone_number(),
            city=city,
            state=state,
            country="United States",
            segment=random.choice(CUSTOMER_SEGMENTS),
            created_at=c_date
        )
        db.add(cust)
        customers.append(cust)
    db.commit()
    logger.info(f"Seeded {len(customers)} customers.")

    logger.info("Seeding orders and order items (spanning 2024 to mid-2026)...")
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2026, 6, 30)
    total_days = (end_date - start_date).days

    orders_count = 0
    items_count = 0

    for _ in range(2600):
        # Generate random date with seasonal distribution
        random_day = random.randint(0, total_days)
        order_date = start_date + timedelta(days=random_day, hours=random.randint(8, 20), minutes=random.randint(0, 59))
        
        # Seasonality multiplier (Q4 holiday boost)
        if order_date.month in [11, 12]:
            if random.random() < 0.35:  # Extra orders in Q4
                new_month = random.choice([11, 12])
                new_day = min(order_date.day, 30 if new_month == 11 else 31)
                order_date = order_date.replace(month=new_month, day=new_day)

        cust = random.choice(customers)
        status = random.choice(ORDER_STATUSES)
        payment = random.choice(PAYMENT_METHODS)

        order = Order(
            customer_id=cust.customer_id,
            order_date=order_date,
            shipping_city=cust.city,
            shipping_state=cust.state,
            shipping_country="United States",
            status=status,
            payment_method=payment,
            total_amount=0.0
        )
        db.add(order)
        db.flush()  # get order_id

        # Generate 1 to 4 order items
        num_items = random.choices([1, 2, 3, 4], weights=[0.5, 0.3, 0.15, 0.05])[0]
        selected_products = random.sample(products, num_items)
        order_total = 0.0

        for prod in selected_products:
            quantity = random.choices([1, 2, 3, 5], weights=[0.7, 0.2, 0.07, 0.03])[0]
            discount = random.choice([0.0, 0.0, 0.0, 0.05, 0.10, 0.15]) if status == "Completed" else 0.0
            item_price = prod.unit_price * (1 - discount)
            item_total = round(item_price * quantity, 2)
            order_total += item_total

            item = OrderItem(
                order_id=order.order_id,
                product_id=prod.product_id,
                quantity=quantity,
                unit_price=prod.unit_price,
                discount=discount,
                total_amount=item_total
            )
            db.add(item)
            items_count += 1

        order.total_amount = round(order_total, 2)
        orders_count += 1

    db.commit()
    logger.info(f"Seeded {orders_count} orders and {items_count} order items successfully.")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
