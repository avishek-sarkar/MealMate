"""
MealMate - Campus Food Hub
A Flask web application for campus food reviews and marketplace
Database-powered version with SQLAlchemy
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_migrate import Migrate
import os
from datetime import datetime, timedelta
import logging

# Import database models
from models import db, User, HotelOwner, MenuItem, Review, StudentFoodPost, cleanup_expired_content

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///mealmate.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    
    # Create upload directory
    os.makedirs(os.path.join(app.root_path, app.config['UPLOAD_FOLDER']), exist_ok=True)
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    with app.app_context():
        # Create database tables
        db.create_all()

    # ==================================================================================
    # UTILITY FUNCTIONS
    # ==================================================================================
    
    def require_login():
        """Check if user is logged in"""
        return 'user_id' in session
    
    def require_hotel_login():
        """Check if hotel owner is logged in"""
        return 'hotel_owner_id' in session
    
    def get_current_user():
        """Get current logged in user"""
        if 'user_id' in session:
            return User.query.get(session['user_id'])
        return None
    
    def get_current_hotel_owner():
        """Get current logged in hotel owner"""
        if 'hotel_owner_id' in session:
            return HotelOwner.query.get(session['hotel_owner_id'])
        return None

    # ==================================================================================
    # MAIN ROUTES
    # ==================================================================================
    
    @app.route('/')
    def index():
        """Home page with newsfeed"""
        # Clean up expired content
        cleanup_expired_content()
        
        # Get recent reviews and food posts
        recent_reviews = Review.query.filter(Review.expires_at > datetime.utcnow()).order_by(Review.created_at.desc()).limit(10).all()
        recent_food_posts = StudentFoodPost.query.filter(StudentFoodPost.expires_at > datetime.utcnow()).order_by(StudentFoodPost.created_at.desc()).limit(10).all()
        available_menu_items = MenuItem.query.filter(MenuItem.expires_at > datetime.utcnow(), MenuItem.is_available == True).order_by(MenuItem.created_at.desc()).limit(5).all()
        
        # Combine and sort by creation time
        all_posts = []
        
        for review in recent_reviews:
            all_posts.append({
                'type': 'review',
                'id': review.id,
                'user': {
                    'name': review.user.username,
                    'avatar': 'https://via.placeholder.com/40x40'
                },
                'rating': review.rating,
                'restaurant': review.menu_item.hotel_owner.hotel_name,
                'menuItem': review.menu_item.item_name,
                'price': review.menu_item.price,
                'comment': review.comment,
                'image': review.image_url or '',
                'likes': 0,
                'comments': 0,
                'timeAgo': get_time_ago(review.created_at),
                'expiresIn': calculate_time_remaining(review.created_at),
                'created_at': review.created_at
            })
        
        for post in recent_food_posts:
            all_posts.append({
                'type': 'homemade',
                'id': post.id,
                'user': {
                    'name': post.user.username,
                    'avatar': 'https://via.placeholder.com/40x40'
                },
                'title': post.title,
                'description': post.description,
                'price': post.price,
                'image': post.image_url or 'https://via.placeholder.com/300x200',
                'location': post.location,
                'isVegetarian': post.food_type == 'veg',
                'servingSize': post.quantity,
                'likes': 0,
                'comments': 0,
                'timeAgo': get_time_ago(post.created_at),
                'expiresIn': calculate_time_remaining(post.created_at),
                'created_at': post.created_at
            })
        
        # Sort by creation time (newest first)
        all_posts.sort(key=lambda x: x['created_at'], reverse=True)
        
        # Get hotel data
        hotels = HotelOwner.query.filter_by(is_verified=True, is_active=True).all()
        hotels_data = []
        for hotel in hotels:
            hotel_data = hotel.to_dict()
            hotel_data['menu_items'] = [item.to_dict() for item in available_menu_items if item.hotel_owner_id == hotel.id]
            hotels_data.append(hotel_data)
        
        return render_template('index.html', 
                             posts=all_posts,
                             hotels=hotels_data,
                             homemade_food=[{
                                 'id': post.id,
                                 'seller': {
                                     'name': post.user.username,
                                     'avatar': 'https://via.placeholder.com/40x40'
                                 },
                                 'title': post.title,
                                 'description': post.description,
                                 'price': post.price,
                                 'image': post.image_url or 'https://via.placeholder.com/300x200',
                                 'location': post.location,
                                 'isVegetarian': post.food_type == 'veg',
                                 'servingSize': post.quantity,
                                 'expiresIn': calculate_time_remaining(post.created_at)
                             } for post in recent_food_posts],
                             current_user=get_current_user() or get_current_hotel_owner())

    # ==================================================================================
    # AUTHENTICATION ROUTES
    # ==================================================================================
    
    @app.route('/register', methods=['POST'])
    def register():
        """Student registration"""
        try:
            # Handle both JSON and form data
            if request.is_json:
                data = request.get_json()
            else:
                data = request.form.to_dict()
            
            # Validate required fields
            required_fields = ['username', 'reg_number', 'email', 'password']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({'success': False, 'message': f'{field} is required'}), 400
            
            # Check if user already exists
            if User.query.filter_by(username=data['username']).first():
                return jsonify({'success': False, 'message': 'Username already exists'}), 400
            
            if User.query.filter_by(email=data['email']).first():
                return jsonify({'success': False, 'message': 'Email already registered'}), 400
            
            if User.query.filter_by(reg_number=data['reg_number']).first():
                return jsonify({'success': False, 'message': 'Registration number already exists'}), 400
            
            # Create new user
            user = User(
                username=data['username'],
                reg_number=data['reg_number'],
                email=data['email']
            )
            user.set_password(data['password'])
            
            db.session.add(user)
            db.session.commit()
            
            # Log in the user
            session['user_id'] = user.id
            session['user_type'] = 'student'
            
            return jsonify({
                'success': True, 
                'message': 'Registration successful',
                'user': user.to_dict()
            })
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Registration error: {str(e)}")
            return jsonify({'success': False, 'message': 'Registration failed'}), 500

    @app.route('/register-hotel', methods=['POST'])
    def register_hotel():
        """Hotel owner registration"""
        try:
            # Handle both JSON and form data
            if request.is_json:
                data = request.get_json()
            else:
                data = request.form.to_dict()
            
            # Validate required fields
            required_fields = ['username', 'hotel_name', 'email', 'hotel_address', 'contact_number', 'license_number', 'password']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({'success': False, 'message': f'{field.replace("_", " ").title()} is required'}), 400
            
            # Check if hotel owner already exists
            if HotelOwner.query.filter_by(username=data['username']).first():
                return jsonify({'success': False, 'message': 'Username already exists'}), 400
            
            if HotelOwner.query.filter_by(email=data['email']).first():
                return jsonify({'success': False, 'message': 'Email already registered'}), 400
            
            if HotelOwner.query.filter_by(license_number=data['license_number']).first():
                return jsonify({'success': False, 'message': 'License number already registered'}), 400
            
            # Create new hotel owner
            hotel_owner = HotelOwner(
                username=data['username'],
                email=data['email'],
                hotel_name=data['hotel_name'],
                hotel_address=data['hotel_address'],
                contact_number=data['contact_number'],
                license_number=data['license_number'],
                is_verified=False  # Requires manual verification
            )
            hotel_owner.set_password(data['password'])
            
            db.session.add(hotel_owner)
            db.session.commit()
            
            # Log in the hotel owner
            session['hotel_owner_id'] = hotel_owner.id
            session['user_type'] = 'hotel'
            
            return jsonify({
                'success': True, 
                'message': 'Registration successful! Your account is pending verification.',
                'user': hotel_owner.to_dict()
            })
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Hotel registration error: {str(e)}")
            return jsonify({'success': False, 'message': 'Registration failed'}), 500
    
    @app.route('/login', methods=['POST'])
    def login():
        """User/Hotel owner login"""
        try:
            # Handle both JSON and form data
            if request.is_json:
                data = request.get_json()
            else:
                data = request.form.to_dict()
            
            username = data.get('username') or data.get('email')
            password = data.get('password')
            user_type = data.get('user_type', 'student')  # student or hotel
            
            if not username or not password:
                return jsonify({'success': False, 'message': 'Username and password required'}), 400
            
            if user_type == 'hotel':
                # Hotel owner login
                hotel_owner = HotelOwner.query.filter(
                    (HotelOwner.username == username) | (HotelOwner.email == username)
                ).first()
                
                if hotel_owner and hotel_owner.check_password(password):
                    session['hotel_owner_id'] = hotel_owner.id
                    session['user_type'] = 'hotel'
                    
                    return jsonify({
                        'success': True,
                        'message': 'Login successful',
                        'user': hotel_owner.to_dict(),
                        'user_type': 'hotel'
                    })
                else:
                    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
            
            else:
                # Student login
                user = User.query.filter(
                    (User.username == username) | (User.email == username)
                ).first()
                
                if user and user.check_password(password):
                    session['user_id'] = user.id
                    session['user_type'] = 'student'
                    
                    return jsonify({
                        'success': True,
                        'message': 'Login successful',
                        'user': user.to_dict(),
                        'user_type': 'student'
                    })
                else:
                    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
                    
        except Exception as e:
            app.logger.error(f"Login error: {str(e)}")
            return jsonify({'success': False, 'message': 'Login failed'}), 500
    
    @app.route('/logout', methods=['GET', 'POST'])
    def logout():
        """Logout user"""
        session.clear()
        
        # For AJAX requests, return JSON
        if request.is_json or request.headers.get('Content-Type') == 'application/json':
            return jsonify({'success': True, 'message': 'Logged out successfully'})
        
        # For regular browser requests, redirect to home page
        return redirect(url_for('index'))

    # ==================================================================================
    # POST-LOGIN FEATURES ROUTES
    # ==================================================================================
    
    @app.route('/post-review', methods=['POST'])
    def post_review():
        """Post a restaurant review (Students only)"""
        if not require_login():
            return jsonify({'success': False, 'message': 'Please login first'}), 401
        
        try:
            # Handle both JSON and form data
            if request.is_json:
                data = request.get_json()
            else:
                data = request.form.to_dict()
            
            # Validate required fields
            required_fields = ['menu_item_id', 'rating', 'comment']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({'success': False, 'message': f'{field.replace("_", " ").title()} is required'}), 400
            
            # Validate rating
            try:
                rating = int(data['rating'])
                if rating < 1 or rating > 5:
                    return jsonify({'success': False, 'message': 'Rating must be between 1 and 5'}), 400
            except ValueError:
                return jsonify({'success': False, 'message': 'Invalid rating value'}), 400
            
            # Check if menu item exists
            menu_item = MenuItem.query.get(data['menu_item_id'])
            if not menu_item:
                return jsonify({'success': False, 'message': 'Menu item not found'}), 404
            
            # Create review
            review = Review(
                user_id=session['user_id'],
                menu_item_id=data['menu_item_id'],
                rating=rating,
                comment=data['comment'],
                image_url=data.get('image_url', '')
            )
            
            db.session.add(review)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Review posted successfully!',
                'review': {
                    'id': review.id,
                    'rating': review.rating,
                    'comment': review.comment,
                    'restaurant': menu_item.hotel_owner.hotel_name,
                    'menu_item': menu_item.item_name
                }
            })
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Review posting error: {str(e)}")
            return jsonify({'success': False, 'message': 'Failed to post review'}), 500
    
    @app.route('/post-food', methods=['POST'])
    def post_food():
        """Post homemade food (Students only)"""
        if not require_login():
            return jsonify({'success': False, 'message': 'Please login first'}), 401
        
        try:
            # Handle both JSON and form data
            if request.is_json:
                data = request.get_json()
            else:
                data = request.form.to_dict()
            
            # Validate required fields
            required_fields = ['title', 'description', 'price', 'quantity', 'location', 'contact_info']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({'success': False, 'message': f'{field.replace("_", " ").title()} is required'}), 400
            
            # Validate price and quantity
            try:
                price = float(data['price'])
                quantity = int(data['quantity'])
                if price <= 0 or quantity <= 0:
                    return jsonify({'success': False, 'message': 'Price and quantity must be greater than 0'}), 400
            except ValueError:
                return jsonify({'success': False, 'message': 'Invalid price or quantity'}), 400
            
            # Create food post
            food_post = StudentFoodPost(
                user_id=session['user_id'],
                title=data['title'],
                description=data['description'],
                price=price,
                quantity=quantity,
                food_type=data.get('food_type', 'veg'),
                cuisine=data.get('cuisine', 'indian'),
                location=data['location'],
                contact_info=data['contact_info'],
                image_url=data.get('image_url', ''),
                is_available=True
            )
            
            db.session.add(food_post)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Food post created successfully!',
                'post': {
                    'id': food_post.id,
                    'title': food_post.title,
                    'price': food_post.price,
                    'location': food_post.location
                }
            })
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Food posting error: {str(e)}")
            return jsonify({'success': False, 'message': 'Failed to post food'}), 500
    
    @app.route('/add-menu-item', methods=['POST'])
    def add_menu_item():
        """Add menu item (Hotel owners only)"""
        if not require_hotel_login():
            return jsonify({'success': False, 'message': 'Please login as hotel owner first'}), 401
        
        try:
            # Handle both JSON and form data
            if request.is_json:
                data = request.get_json()
            else:
                data = request.form.to_dict()
            
            # Validate required fields
            required_fields = ['item_name', 'description', 'price', 'category']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({'success': False, 'message': f'{field.replace("_", " ").title()} is required'}), 400
            
            # Validate price
            try:
                price = float(data['price'])
                if price <= 0:
                    return jsonify({'success': False, 'message': 'Price must be greater than 0'}), 400
            except ValueError:
                return jsonify({'success': False, 'message': 'Invalid price value'}), 400
            
            # Create menu item
            menu_item = MenuItem(
                hotel_owner_id=session['hotel_owner_id'],
                item_name=data['item_name'],
                description=data['description'],
                price=price,
                category=data['category'],
                image_url=data.get('image_url', ''),
                is_available=True
            )
            
            db.session.add(menu_item)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Menu item added successfully!',
                'item': {
                    'id': menu_item.id,
                    'name': menu_item.item_name,
                    'price': menu_item.price,
                    'category': menu_item.category
                }
            })
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Menu item creation error: {str(e)}")
            return jsonify({'success': False, 'message': 'Failed to add menu item'}), 500
    
    @app.route('/update-menu-item/<int:item_id>', methods=['PUT'])
    def update_menu_item(item_id):
        """Update menu item (Hotel owners only)"""
        if not require_hotel_login():
            return jsonify({'success': False, 'message': 'Please login as hotel owner first'}), 401
        
        try:
            # Find menu item
            menu_item = MenuItem.query.filter_by(id=item_id, hotel_owner_id=session['hotel_owner_id']).first()
            if not menu_item:
                return jsonify({'success': False, 'message': 'Menu item not found'}), 404
            
            # Handle both JSON and form data
            if request.is_json:
                data = request.get_json()
            else:
                data = request.form.to_dict()
            
            # Update fields if provided
            if 'item_name' in data:
                menu_item.item_name = data['item_name']
            if 'description' in data:
                menu_item.description = data['description']
            if 'price' in data:
                try:
                    price = float(data['price'])
                    if price <= 0:
                        return jsonify({'success': False, 'message': 'Price must be greater than 0'}), 400
                    menu_item.price = price
                except ValueError:
                    return jsonify({'success': False, 'message': 'Invalid price value'}), 400
            if 'category' in data:
                menu_item.category = data['category']
            if 'image_url' in data:
                menu_item.image_url = data['image_url']
            if 'is_available' in data:
                menu_item.is_available = data['is_available'].lower() in ['true', '1', 'yes']
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Menu item updated successfully!',
                'item': menu_item.to_dict()
            })
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Menu item update error: {str(e)}")
            return jsonify({'success': False, 'message': 'Failed to update menu item'}), 500
    
    @app.route('/my-menu', methods=['GET'])
    def my_menu():
        """Get menu items for current hotel owner"""
        if not require_hotel_login():
            return jsonify({'success': False, 'message': 'Please login as hotel owner first'}), 401
        
        try:
            menu_items = MenuItem.query.filter_by(hotel_owner_id=session['hotel_owner_id']).order_by(MenuItem.created_at.desc()).all()
            
            return jsonify({
                'success': True,
                'menu_items': [item.to_dict() for item in menu_items]
            })
            
        except Exception as e:
            app.logger.error(f"Menu fetch error: {str(e)}")
            return jsonify({'success': False, 'message': 'Failed to fetch menu'}), 500
    
    @app.route('/my-posts', methods=['GET'])
    def my_posts():
        """Get posts for current user"""
        if not require_login():
            return jsonify({'success': False, 'message': 'Please login first'}), 401
        
        try:
            # Get user's reviews
            reviews = Review.query.filter_by(user_id=session['user_id']).order_by(Review.created_at.desc()).all()
            
            # Get user's food posts
            food_posts = StudentFoodPost.query.filter_by(user_id=session['user_id']).order_by(StudentFoodPost.created_at.desc()).all()
            
            review_data = []
            for review in reviews:
                review_data.append({
                    'id': review.id,
                    'type': 'review',
                    'rating': review.rating,
                    'comment': review.comment,
                    'restaurant': review.menu_item.hotel_owner.hotel_name,
                    'menu_item': review.menu_item.item_name,
                    'created_at': review.created_at.isoformat(),
                    'timeAgo': get_time_ago(review.created_at)
                })
            
            food_data = []
            for post in food_posts:
                food_data.append({
                    'id': post.id,
                    'type': 'food',
                    'title': post.title,
                    'description': post.description,
                    'price': post.price,
                    'location': post.location,
                    'contact_info': post.contact_info,
                    'is_available': post.is_available,
                    'created_at': post.created_at.isoformat(),
                    'timeAgo': get_time_ago(post.created_at)
                })
            
            return jsonify({
                'success': True,
                'reviews': review_data,
                'food_posts': food_data
            })
            
        except Exception as e:
            app.logger.error(f"Posts fetch error: {str(e)}")
            return jsonify({'success': False, 'message': 'Failed to fetch posts'}), 500

    @app.route('/api/menu-items/<int:hotel_id>')
    def api_menu_items(hotel_id):
        """Get menu items for a specific hotel"""
        try:
            menu_items = MenuItem.query.filter_by(
                hotel_owner_id=hotel_id, 
                is_available=True
            ).filter(MenuItem.expires_at > datetime.utcnow()).all()
            
            return jsonify([item.to_dict() for item in menu_items])
            
        except Exception as e:
            app.logger.error(f"Menu items fetch error: {str(e)}")
            return jsonify([])

    @app.route('/update-profile', methods=['PUT', 'POST'])
    def update_profile():
        """Update user profile (Students only)"""
        if not require_login():
            return jsonify({'success': False, 'message': 'Please login first'}), 401
        
        try:
            # Handle both JSON and form data
            if request.is_json:
                data = request.get_json()
            else:
                data = request.form.to_dict()
            
            user = User.query.get(session['user_id'])
            if not user:
                return jsonify({'success': False, 'message': 'User not found'}), 404
            
            # Update fields if provided
            if 'username' in data and data['username'] != user.username:
                # Check if username is already taken
                if User.query.filter_by(username=data['username']).first():
                    return jsonify({'success': False, 'message': 'Username already exists'}), 400
                user.username = data['username']
            
            if 'email' in data and data['email'] != user.email:
                # Check if email is already taken
                if User.query.filter_by(email=data['email']).first():
                    return jsonify({'success': False, 'message': 'Email already exists'}), 400
                user.email = data['email']
            
            if 'reg_number' in data and data['reg_number'] != user.reg_number:
                # Check if reg_number is already taken
                if User.query.filter_by(reg_number=data['reg_number']).first():
                    return jsonify({'success': False, 'message': 'Registration number already exists'}), 400
                user.reg_number = data['reg_number']
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Profile updated successfully!',
                'user': user.to_dict()
            })
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Profile update error: {str(e)}")
            return jsonify({'success': False, 'message': 'Failed to update profile'}), 500

    @app.route('/update-business', methods=['PUT', 'POST'])
    def update_business():
        """Update business profile (Hotel owners only)"""
        if not require_hotel_login():
            return jsonify({'success': False, 'message': 'Please login as hotel owner first'}), 401
        
        try:
            # Handle both JSON and form data
            if request.is_json:
                data = request.get_json()
            else:
                data = request.form.to_dict()
            
            hotel_owner = HotelOwner.query.get(session['hotel_owner_id'])
            if not hotel_owner:
                return jsonify({'success': False, 'message': 'Hotel owner not found'}), 404
            
            # Update fields if provided
            if 'username' in data and data['username'] != hotel_owner.username:
                # Check if username is already taken
                if HotelOwner.query.filter_by(username=data['username']).first():
                    return jsonify({'success': False, 'message': 'Username already exists'}), 400
                hotel_owner.username = data['username']
            
            if 'email' in data and data['email'] != hotel_owner.email:
                # Check if email is already taken
                if HotelOwner.query.filter_by(email=data['email']).first():
                    return jsonify({'success': False, 'message': 'Email already exists'}), 400
                hotel_owner.email = data['email']
            
            if 'hotel_name' in data:
                hotel_owner.hotel_name = data['hotel_name']
            
            if 'hotel_address' in data:
                hotel_owner.hotel_address = data['hotel_address']
            
            if 'contact_number' in data:
                hotel_owner.contact_number = data['contact_number']
            
            if 'license_number' in data and data['license_number'] != hotel_owner.license_number:
                # Check if license number is already taken
                if HotelOwner.query.filter_by(license_number=data['license_number']).first():
                    return jsonify({'success': False, 'message': 'License number already exists'}), 400
                hotel_owner.license_number = data['license_number']
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Business information updated successfully!',
                'business': hotel_owner.to_dict()
            })
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Business update error: {str(e)}")
            return jsonify({'success': False, 'message': 'Failed to update business information'}), 500

    @app.route('/change-password', methods=['PUT', 'POST'])
    def change_password():
        """Change password for students"""
        if not require_login():
            return jsonify({'success': False, 'message': 'Please login first'}), 401
        
        try:
            # Handle both JSON and form data
            if request.is_json:
                data = request.get_json()
            else:
                data = request.form.to_dict()
            
            # Validate required fields
            required_fields = ['current_password', 'new_password', 'confirm_password']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({'success': False, 'message': f'{field.replace("_", " ").title()} is required'}), 400
            
            user = User.query.get(session['user_id'])
            if not user:
                return jsonify({'success': False, 'message': 'User not found'}), 404
            
            # Check current password
            if not user.check_password(data['current_password']):
                return jsonify({'success': False, 'message': 'Current password is incorrect'}), 400
            
            # Check if new passwords match
            if data['new_password'] != data['confirm_password']:
                return jsonify({'success': False, 'message': 'New passwords do not match'}), 400
            
            # Update password
            user.set_password(data['new_password'])
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Password changed successfully!'
            })
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Password change error: {str(e)}")
            return jsonify({'success': False, 'message': 'Failed to change password'}), 500

    @app.route('/change-hotel-password', methods=['PUT', 'POST'])
    def change_hotel_password():
        """Change password for hotel owners"""
        if not require_hotel_login():
            return jsonify({'success': False, 'message': 'Please login as hotel owner first'}), 401
        
        try:
            # Handle both JSON and form data
            if request.is_json:
                data = request.get_json()
            else:
                data = request.form.to_dict()
            
            # Validate required fields
            required_fields = ['current_password', 'new_password', 'confirm_password']
            for field in required_fields:
                if not data.get(field):
                    return jsonify({'success': False, 'message': f'{field.replace("_", " ").title()} is required'}), 400
            
            hotel_owner = HotelOwner.query.get(session['hotel_owner_id'])
            if not hotel_owner:
                return jsonify({'success': False, 'message': 'Hotel owner not found'}), 404
            
            # Check current password
            if not hotel_owner.check_password(data['current_password']):
                return jsonify({'success': False, 'message': 'Current password is incorrect'}), 400
            
            # Check if new passwords match
            if data['new_password'] != data['confirm_password']:
                return jsonify({'success': False, 'message': 'New passwords do not match'}), 400
            
            # Update password
            hotel_owner.set_password(data['new_password'])
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Password changed successfully!'
            })
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Hotel password change error: {str(e)}")
            return jsonify({'success': False, 'message': 'Failed to change password'}), 500

    @app.route('/get-profile')
    def get_profile():
        """Get current user profile"""
        if require_login():
            user = User.query.get(session['user_id'])
            if user:
                return jsonify({'success': True, 'user': user.to_dict(), 'type': 'student'})
        
        if require_hotel_login():
            hotel_owner = HotelOwner.query.get(session['hotel_owner_id'])
            if hotel_owner:
                return jsonify({'success': True, 'user': hotel_owner.to_dict(), 'type': 'hotel'})
        
        return jsonify({'success': False, 'message': 'Not logged in'}), 401

    # ==================================================================================
    # LEGACY API ROUTES (for backward compatibility)
    # ==================================================================================
    
    @app.route('/api/posts')
    def api_posts():
        """Legacy API endpoint for posts with optional filtering"""
        cleanup_expired_content()
        
        post_type = request.args.get('type', 'all')
        
        # Get data from database
        reviews = Review.query.filter(Review.expires_at > datetime.utcnow()).order_by(Review.created_at.desc()).all()
        food_posts = StudentFoodPost.query.filter(StudentFoodPost.expires_at > datetime.utcnow()).order_by(StudentFoodPost.created_at.desc()).all()
        
        # Convert to legacy format
        legacy_posts = []
        
        for review in reviews:
            if post_type == 'all' or post_type == 'review':
                legacy_posts.append({
                    'id': str(review.id),
                    'type': 'review',
                    'user': {'username': review.user.username},
                    'rating': review.rating,
                    'restaurant': review.menu_item.hotel_owner.hotel_name,
                    'menuItem': review.menu_item.item_name,
                    'price': review.menu_item.price,
                    'comment': review.comment,
                    'image': review.image_url or '',
                    'likes': 0,  # Placeholder
                    'comments': 0,  # Placeholder
                    'created_at': review.created_at,
                    'timeAgo': get_time_ago(review.created_at),
                    'expiresIn': calculate_time_remaining(review.created_at)
                })
        
        for post in food_posts:
            if post_type == 'all' or post_type == 'homemade':
                legacy_posts.append({
                    'id': str(post.id),
                    'type': 'homemade',
                    'user': {'username': post.user.username},
                    'title': post.title,
                    'description': post.description,
                    'price': post.price,
                    'image': post.image_url or '',
                    'location': post.location,
                    'isVegetarian': post.food_type == 'veg',
                    'servingSize': post.quantity,
                    'likes': 0,  # Placeholder
                    'comments': 0,  # Placeholder
                    'created_at': post.created_at,
                    'timeAgo': get_time_ago(post.created_at),
                    'expiresIn': calculate_time_remaining(post.created_at)
                })
        
        # Sort by creation time
        legacy_posts.sort(key=lambda x: x['created_at'], reverse=True)
        
        return jsonify(legacy_posts)

    @app.route('/api/hotels')
    def api_hotels():
        """Legacy API endpoint for hotels"""
        hotels = HotelOwner.query.filter_by(is_verified=True, is_active=True).all()
        
        hotels_data = []
        for hotel in hotels:
            menu_items = MenuItem.query.filter(MenuItem.hotel_owner_id == hotel.id, MenuItem.is_available == True, MenuItem.expires_at > datetime.utcnow()).all()
            
            hotels_data.append({
                'id': hotel.id,
                'name': hotel.hotel_name,
                'address': hotel.hotel_address,
                'contact': hotel.contact_number,
                'rating': 4.2,  # Placeholder
                'image': 'https://via.placeholder.com/300x200',  # Placeholder
                'menu_items': [item.to_dict() for item in menu_items]
            })
        
        return jsonify(hotels_data)

    @app.route('/api/homemade-food')
    def api_homemade_food():
        """Legacy API endpoint for homemade food with sorting"""
        cleanup_expired_content()
        
        sort_by = request.args.get('sort', 'latest')
        
        posts = StudentFoodPost.query.filter(StudentFoodPost.is_available == True, StudentFoodPost.expires_at > datetime.utcnow()).all()
        
        # Sort based on parameter
        if sort_by == 'price-low':
            posts.sort(key=lambda x: x.price)
        elif sort_by == 'price-high':
            posts.sort(key=lambda x: x.price, reverse=True)
        elif sort_by == 'location':
            posts.sort(key=lambda x: x.location)
        else:  # latest
            posts.sort(key=lambda x: x.created_at, reverse=True)
        
        # Convert to legacy format
        legacy_posts = []
        for post in posts:
            legacy_posts.append({
                'id': str(post.id),
                'seller': {'username': post.user.username, 'avatar': 'https://via.placeholder.com/40x40'},
                'title': post.title,
                'description': post.description,
                'price': post.price,
                'image': post.image_url or 'https://via.placeholder.com/300x200',
                'location': post.location,
                'isVegetarian': post.food_type == 'veg',
                'servingSize': post.quantity,
                'created_at': post.created_at,
                'expiresIn': calculate_time_remaining(post.created_at)
            })
        
        return jsonify(legacy_posts)

    # ==================================================================================
    # UTILITY FUNCTIONS (Legacy support)
    # ==================================================================================
    
    def calculate_time_remaining(created_at):
        """Calculate time remaining until 24-hour expiry"""
        expires_at = created_at + timedelta(hours=24)
        remaining = expires_at - datetime.utcnow()
        
        if remaining.total_seconds() <= 0:
            return "Expired"
        
        hours = int(remaining.total_seconds() // 3600)
        if hours <= 0:
            minutes = int((remaining.total_seconds() % 3600) // 60)
            return f"{minutes}m left"
        
        return f"{hours}h left"

    def get_time_ago(created_at):
        """Get human-readable time ago string"""
        diff = datetime.utcnow() - created_at
        hours = int(diff.total_seconds() // 3600)
        
        if hours == 0:
            minutes = int(diff.total_seconds() // 60)
            if minutes == 0:
                return "Just now"
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        elif hours < 24:
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        else:
            days = hours // 24
            return f"{days} day{'s' if days > 1 else ''} ago"

    # ==================================================================================
    # ERROR HANDLERS
    # ==================================================================================
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'success': False, 'message': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

    return app

# Create the app instance
app = create_app()
