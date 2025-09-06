"""
Database initialization script for MealMate
Run this script to set up the database with initial data
"""

from app import app
from models import db, User, HotelOwner, MenuItem, Review, StudentFoodPost, Admin
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
        
        # Create admin user
        admin = Admin(
            username='admin',
            email='admin@mealmate.com'
        )
        admin.set_password('admin123')
        admin.is_super_admin = True
        
        db.session.add(admin)
        db.session.commit()
        
        # Create sample users (initially not approved)
        users = [
            User(username='avishek_sarkar', reg_number='9902', email='avishek_21102035@jkkniu.edu.bd'),
            User(username='tamim5', reg_number='9908', email='tamim@jkkniu.edu.bd'),
            User(username='mridula', reg_number='9890', email='mridulabtv@jkkniu.edu.bd'),
        ]
        
        for user in users:
            user.set_password('password123')
            # Initially not approved - admin needs to approve
            user.is_approved = False
        
        db.session.add_all(users)
        db.session.commit()
        
        # Auto-approve the first user for demonstration
        users[0].is_approved = True
        users[0].approved_by = admin.id
        users[0].approved_at = datetime.utcnow()
        
        # Create sample hotel owners (initially not approved)
        hotels = [
            HotelOwner(
                username='hotel_sareng',
                email='owner@hotelsareng.com',
                hotel_name='Hotel Sareng',
                hotel_address='Main Road, Trishal Campus Area, Mymensingh',
                contact_number='+880-1712345678',
                license_number='BSTI54321',
                is_verified=False,
                is_approved=False  # Admin needs to approve
            ),
            HotelOwner(
                username='mastercafe',
                email='owner@mastercafe.com',
                hotel_name='MasterCafe',
                hotel_address='University Gate, Trishal Campus, Mymensingh',
                contact_number='+880-1812345679',
                license_number='BSTI54322',
                is_verified=False,
                is_approved=False  # Admin needs to approve
            ),
            HotelOwner(
                username='chondrobindu',
                email='owner@chondrobindu.com',
                hotel_name='Chondrobindu',
                hotel_address='Student Area, Trishal Campus Road, Mymensingh',
                contact_number='+880-1912345680',
                license_number='BSTI54323',
                is_verified=False,
                is_approved=False  # Admin needs to approve
            ),
        ]
        
        for hotel in hotels:
            hotel.set_password('hotel123')
        
        db.session.add_all(hotels)
        db.session.commit()
        
        # Auto-approve the first hotel for demonstration
        hotels[0].is_approved = True
        hotels[0].is_verified = True
        hotels[0].approved_by = admin.id
        hotels[0].approved_at = datetime.utcnow()
        
        db.session.commit()
        
        # Create sample menu items
        menu_items = [
            # Hotel Sareng items
            MenuItem(
                hotel_owner_id=hotels[0].id,
                item_name='Special Beef Biriyani',
                description='Traditional beef biriyani with basmati rice and aromatic spices',
                price=200.0,
                category='lunch',
                is_available=True
            ),
            MenuItem(
                hotel_owner_id=hotels[0].id,
                item_name='Chicken Curry with Rice',
                description='Spicy Bengali chicken curry served with steamed rice',
                price=150.0,
                category='lunch',
                is_available=True
            ),
            MenuItem(
                hotel_owner_id=hotels[0].id,
                item_name='Mixed Vegetable Curry',
                description='Fresh seasonal vegetables cooked in traditional Bengali style',
                price=90.0,
                category='lunch',
                is_available=True
            ),
            
            # MasterCafe items
            MenuItem(
                hotel_owner_id=hotels[1].id,
                item_name='Chicken Fried Rice',
                description='Wok-fried rice with chicken, vegetables and special sauce',
                price=120.0,
                category='lunch',
                is_available=True
            ),
            MenuItem(
                hotel_owner_id=hotels[1].id,
                item_name='Beef Burger',
                description='Juicy beef burger with fresh vegetables and french fries',
                price=180.0,
                category='snacks',
                is_available=True
            ),
            MenuItem(
                hotel_owner_id=hotels[1].id,
                item_name='Cold Coffee',
                description='Refreshing iced coffee with milk and sugar',
                price=60.0,
                category='beverages',
                is_available=True
            ),
            
            # Chondrobindu items
            MenuItem(
                hotel_owner_id=hotels[2].id,
                item_name='Hilsha Fish Curry',
                description='Premium hilsha fish curry with authentic Bengali spices',
                price=220.0,
                category='lunch',
                is_available=True
            ),
            MenuItem(
                hotel_owner_id=hotels[2].id,
                item_name='Dal Fry with Rice',
                description='Yellow lentil curry with fried onions served with rice',
                price=80.0,
                category='lunch',
                is_available=True
            ),
            MenuItem(
                hotel_owner_id=hotels[2].id,
                item_name='Mango Lassi',
                description='Sweet mango yogurt drink with traditional flavor',
                price=45.0,
                category='beverages',
                is_available=True
            ),
        ]
        
        db.session.add_all(menu_items)
        db.session.commit()
        
        # Create sample reviews
        reviews = [
            Review(
                user_id=users[0].id,  # avishek_sarkar
                menu_item_id=menu_items[0].id,  # Hotel Sareng's Special Beef Biriyani
                rating=5,
                comment='Outstanding beef biriyani! The meat was tender and spices were perfectly balanced.'
            ),
            Review(
                user_id=users[1].id,  # tamim5
                menu_item_id=menu_items[3].id,  # MasterCafe's Chicken Fried Rice
                rating=4,
                comment='Great fried rice with good portion size. Perfect for lunch!'
            ),
            Review(
                user_id=users[2].id,  # mridula
                menu_item_id=menu_items[6].id,  # Chondrobindu's Hilsha Fish Curry
                rating=5,
                comment='Amazing hilsha fish curry! Tastes like homemade food. Highly recommended!'
            ),
            Review(
                user_id=users[0].id,  # avishek_sarkar
                menu_item_id=menu_items[4].id,  # MasterCafe's Beef Burger
                rating=4,
                comment='Delicious burger with fresh ingredients. The fries were crispy too.'
            ),
        ]
        
        db.session.add_all(reviews)
        db.session.commit()
        
        # Create sample student food posts
        food_posts = [
            StudentFoodPost(
                user_id=users[1].id,  # tamim5
                title='Homemade Chicken Biriyani',
                description='Authentic Bangladeshi chicken biriyani with aromatic spices and borhani',
                price=70.0,
                quantity=4,
                food_type='non-veg',
                cuisine='bangladeshi',
                location='Trishal Boys Hostel A, Room 204',
                contact_info='tamim5 (WhatsApp: +880-1712345678)'
            ),
            StudentFoodPost(
                user_id=users[2].id,  # mridula
                title='Chitoi Pitha with Kheer',
                description='Traditional rice cakes with sweet milk pudding, homemade style',
                price=35.0,
                quantity=8,
                food_type='veg',
                cuisine='bangladeshi',
                location='Trishal Girls Hostel B, Room 315',
                contact_info='mridula (Call: +880-1812345679)'
            ),
            StudentFoodPost(
                user_id=users[0].id,  # avishek_sarkar
                title='Fish Curry & Rice',
                description='Traditional Bengali rui fish curry with steamed rice and mixed vegetables',
                price=50.0,
                quantity=5,
                food_type='non-veg',
                cuisine='bangladeshi',
                location='Trishal Campus Hostel C, Room 108',
                contact_info='avishek_sarkar (WhatsApp: +880-1912345680)'
            ),
            StudentFoodPost(
                user_id=users[1].id,  # tamim5
                title='Beef Tehari',
                description='Spicy beef tehari with fried onions and traditional spices',
                price=60.0,
                quantity=6,
                food_type='non-veg',
                cuisine='bangladeshi',
                location='Trishal Campus Hostel D, Room 227',
                contact_info='tamim5 (WhatsApp: +880-1712345681)'
            ),
        ]
        
        db.session.add_all(food_posts)
        db.session.commit()
        
        print("✅ Database initialized successfully!")
        print(f"Created 1 admin user")
        print(f"Created {len(users)} users")
        print(f"Created {len(hotels)} hotel owners")
        print(f"Created {len(menu_items)} menu items")
        print(f"Created {len(reviews)} reviews")
        print(f"Created {len(food_posts)} student food posts")
        
        print("\n🔐 Default login credentials:")
        print("Admin: admin / admin123")
        print("Students: avishek_sarkar / tamim5 / mridula")
        print("Password: password123")
        print("\nHotel Owners: hotel_sareng / mastercafe / chondrobindu")
        print("Password: hotel123")
        print("\n⚠️  Note: Most users and hotels require admin approval before they can fully use the system.")

if __name__ == '__main__':
    init_database()
