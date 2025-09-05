"""
Database initialization script for MealMate
Run this script to set up the database with initial data
"""

from app import app
from models import db, User, HotelOwner, MenuItem, Review, StudentFoodPost
from datetime import datetime

def init_database():
    """Initialize database with sample data"""
    with app.app_context():
        # Drop all tables and recreate them
        print("Dropping existing tables...")
        db.drop_all()
        
        print("Creating new tables...")
        db.create_all()
        
        print("Creating sample data...")
        
        # Create sample users
        users = [
            User(username='john_doe', reg_number='2023CSE001', email='john@university.edu'),
            User(username='jane_smith', reg_number='2023CSE002', email='jane@university.edu'),
            User(username='mike_wilson', reg_number='2023CSE003', email='mike@university.edu'),
            User(username='sarah_jones', reg_number='2023CSE004', email='sarah@university.edu'),
        ]
        
        for user in users:
            user.set_password('password123')
        
        db.session.add_all(users)
        db.session.commit()
        
        # Create sample hotel owners
        hotels = [
            HotelOwner(
                username='pizza_palace',
                email='owner@pizzapalace.com',
                hotel_name='Pizza Palace',
                hotel_address='Near Main Gate, University Road',
                contact_number='+91-9876543210',
                license_number='FSSAI12345',
                is_verified=True
            ),
            HotelOwner(
                username='burger_house',
                email='owner@burgerhouse.com',
                hotel_name='Burger House',
                hotel_address='Opposite Library, Campus Road',
                contact_number='+91-9876543211',
                license_number='FSSAI12346',
                is_verified=True
            ),
            HotelOwner(
                username='south_delights',
                email='owner@southdelights.com',
                hotel_name='South Delights',
                hotel_address='Food Court, Student Center',
                contact_number='+91-9876543212',
                license_number='FSSAI12347',
                is_verified=True
            ),
        ]
        
        for hotel in hotels:
            hotel.set_password('hotel123')
        
        db.session.add_all(hotels)
        db.session.commit()
        
        # Create sample menu items
        menu_items = [
            # Pizza Palace items
            MenuItem(
                hotel_owner_id=hotels[0].id,
                item_name='Margherita Pizza',
                description='Fresh tomatoes, mozzarella cheese, basil',
                price=299.0,
                category='lunch',
                is_available=True
            ),
            MenuItem(
                hotel_owner_id=hotels[0].id,
                item_name='Pepperoni Pizza',
                description='Spicy pepperoni with cheese',
                price=349.0,
                category='lunch',
                is_available=True
            ),
            MenuItem(
                hotel_owner_id=hotels[0].id,
                item_name='Garlic Bread',
                description='Crispy bread with garlic butter',
                price=99.0,
                category='snacks',
                is_available=True
            ),
            
            # Burger House items
            MenuItem(
                hotel_owner_id=hotels[1].id,
                item_name='Chicken Burger',
                description='Grilled chicken patty with lettuce and mayo',
                price=149.0,
                category='snacks',
                is_available=True
            ),
            MenuItem(
                hotel_owner_id=hotels[1].id,
                item_name='Cheese Burger',
                description='Beef patty with cheese and vegetables',
                price=169.0,
                category='snacks',
                is_available=True
            ),
            MenuItem(
                hotel_owner_id=hotels[1].id,
                item_name='French Fries',
                description='Crispy golden fries',
                price=79.0,
                category='snacks',
                is_available=True
            ),
            
            # South Delights items
            MenuItem(
                hotel_owner_id=hotels[2].id,
                item_name='Masala Dosa',
                description='Crispy dosa with spiced potato filling',
                price=89.0,
                category='breakfast',
                is_available=True
            ),
            MenuItem(
                hotel_owner_id=hotels[2].id,
                item_name='Chicken Biryani',
                description='Aromatic basmati rice with chicken',
                price=199.0,
                category='lunch',
                is_available=True
            ),
            MenuItem(
                hotel_owner_id=hotels[2].id,
                item_name='Filter Coffee',
                description='Traditional South Indian coffee',
                price=25.0,
                category='beverages',
                is_available=True
            ),
        ]
        
        db.session.add_all(menu_items)
        db.session.commit()
        
        # Create sample reviews
        reviews = [
            Review(
                user_id=users[0].id,
                menu_item_id=menu_items[0].id,
                rating=4,
                comment='Great pizza! Fresh ingredients and good taste.'
            ),
            Review(
                user_id=users[1].id,
                menu_item_id=menu_items[3].id,
                rating=5,
                comment='Best chicken burger on campus! Highly recommended.'
            ),
            Review(
                user_id=users[2].id,
                menu_item_id=menu_items[6].id,
                rating=4,
                comment='Authentic South Indian taste. Reminded me of home.'
            ),
            Review(
                user_id=users[3].id,
                menu_item_id=menu_items[1].id,
                rating=3,
                comment='Good pizza but a bit too spicy for my taste.'
            ),
        ]
        
        db.session.add_all(reviews)
        db.session.commit()
        
        # Create sample student food posts
        food_posts = [
            StudentFoodPost(
                user_id=users[1].id,
                title='Homemade Biryani',
                description='Authentic Hyderabadi chicken biryani made with love',
                price=80.0,
                quantity=5,
                food_type='non-veg',
                cuisine='indian',
                location='Hostel A, Room 204',
                contact_info='jane_smith (WhatsApp: 9876543210)'
            ),
            StudentFoodPost(
                user_id=users[2].id,
                title='Mom\'s Special Aloo Paratha',
                description='Fresh aloo parathas with pickle and curd',
                price=40.0,
                quantity=8,
                food_type='veg',
                cuisine='north-indian',
                location='Hostel B, Room 315',
                contact_info='mike_wilson (Call: 9876543211)'
            ),
            StudentFoodPost(
                user_id=users[3].id,
                title='Chocolate Brownies',
                description='Freshly baked chocolate brownies',
                price=25.0,
                quantity=12,
                food_type='veg',
                cuisine='dessert',
                location='Girls Hostel, Room 108',
                contact_info='sarah_jones (WhatsApp: 9876543212)'
            ),
            StudentFoodPost(
                user_id=users[0].id,
                title='Rajma Chawal',
                description='Homestyle rajma with steamed rice',
                price=60.0,
                quantity=6,
                food_type='veg',
                cuisine='north-indian',
                location='Hostel C, Room 227',
                contact_info='john_doe (WhatsApp: 9876543213)'
            ),
        ]
        
        db.session.add_all(food_posts)
        db.session.commit()
        
        print("✅ Database initialized successfully!")
        print(f"Created {len(users)} users")
        print(f"Created {len(hotels)} hotel owners")
        print(f"Created {len(menu_items)} menu items")
        print(f"Created {len(reviews)} reviews")
        print(f"Created {len(food_posts)} student food posts")
        
        print("\n🔐 Default login credentials:")
        print("Students: john_doe / jane_smith / mike_wilson / sarah_jones")
        print("Password: password123")
        print("\nHotel Owners: pizza_palace / burger_house / south_delights")
        print("Password: hotel123")

if __name__ == '__main__':
    init_database()
