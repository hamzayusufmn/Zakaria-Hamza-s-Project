# seed_data.py

from app import app
from extensions import db
from models.menu import Category, MenuItem
from models.hours import Hours

with app.app_context():
    # 1) Ensure categories exist and create if not 
    if Category.query.count() == 0:
        c1 = Category(name="Appetizers",    display_order=1)
        c2 = Category(name="Main Courses",  display_order=2)
        c3 = Category(name="Drinks",        display_order=3)
        c4 = Category(name="Desserts",      display_order=4)
        db.session.add_all([c1, c2, c3, c4])
        db.session.commit()
        print("Categories seeded.")
    else:
        print(" Categories already exist, skipping.")

    # 2) Now seed items only if none exist/ used this to check if i had this and makes it easier if someone
    # wants the data and can just run this one command 
    if MenuItem.query.count() == 0:
        cats = {c.name: c.id for c in Category.query.all()}
        items = [
            MenuItem(name="Stuffed Grape Leaves", description="Vine leaves & herbs", price=6.50,
                     image_path="appetizer1.jpg", category_id=cats["Appetizers"]),
            MenuItem(name="Falafel with Tahini",   description="Chickpea fritters",  price=7.00,
                     image_path="appetizer2.jpg", category_id=cats["Appetizers"]),
            MenuItem(name="Hummus & Pita",         description="Creamy dip + pita",   price=5.50,
                     image_path="appetizer3.jpg", category_id=cats["Appetizers"]),

            MenuItem(name="Chicken Shawarma",      description="Spiced chicken wrap",  price=12.99,
                     image_path="main1.jpg",      category_id=cats["Main Courses"]),
            MenuItem(name="Lamb Gyro",             description="Gyro meat & fries in pita", price=13.50,
                     image_path="main2.jpg",      category_id=cats["Main Courses"]),
            MenuItem(name="Grilled Seafood",       description="Mixed fish & shrimp",  price=18.00,
                     image_path="main3.jpg",      category_id=cats["Main Courses"]),

            MenuItem(name="Mint Lemonade",         description="Fresh mint & lemon",    price=3.50,
                     image_path="drink1.jpg",     category_id=cats["Drinks"]),
            MenuItem(name="Orange Juice",          description="Cold-squeezed OJ",       price=3.00,
                     image_path="drink2.jpg",     category_id=cats["Drinks"]),

            MenuItem(name="Baklava",               description="Honey-drizzled phyllo",  price=4.50,
                     image_path="dessert.jpg",     category_id=cats["Desserts"]),
        ]
        db.session.add_all(items)
        db.session.commit()
        print("✅ Menu items seeded.")
    else:
        print("⚠️  Menu items already exist, skipping.")

    # 3) Seed hours if none exist
    if Hours.query.count() == 0:
        default_hours = [
          ("Monday",    "9:00 AM",  "12:00 AM"),
          ("Tuesday",   "9:00 AM",  "12:00 AM"),
          ("Wednesday", "9:00 AM",  "12:00 AM"),
          ("Thursday",  "9:00 AM",  "12:00 AM"),
          ("Friday",    "9:00 AM",  "12:00 AM"),
          ("Saturday",  "9:00 AM",  "12:00 AM"),
          ("Sunday",    "9:00 AM",  "12:00 AM"),
        ]
        for day, open_t, close_t in default_hours:
            h = Hours(
                day_of_week=day,
                open_time=open_t,
                close_time=close_t,
                is_closed=False,
                is_special=False
            )
            db.session.add(h)
        db.session.commit()
        print("✅ Hours seeded.")
    else:
        print("⚠️  Hours already exist, skipping.")

        # messaage to look for would be like this
        # Categories already exist, skipping.  
        # categories seeded.
        # Menu items already exist, skipping.
        # ✅ Menu items seeded.
        # ✅ Hours seeded.
