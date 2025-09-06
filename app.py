"""
MealMate - Campus Food Hub
A Flask web application for campus food reviews and marketplace
Database-powered version with SQLAlchemy
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_migrate import Migrate
from flask_socketio import SocketIO, emit, join_room, leave_room
import os
from datetime import datetime, timedelta
import logging

# Import database models
from models import db, User, HotelOwner, MenuItem, Review, StudentFoodPost, Admin, Notification, PostInteraction, cleanup_expired_content

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
    
    # Initialize SocketIO for real-time notifications
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')
    app.socketio = socketio  # Store reference for use in routes
    
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
    
    def require_admin_login():
        """Check if admin is logged in"""
        return 'admin_id' in session
    
    def get_current_user():
        """Get current logged in user (student or hotel owner)"""
        if 'user_id' in session:
            return User.query.get(session['user_id'])
        elif 'hotel_owner_id' in session:
            return HotelOwner.query.get(session['hotel_owner_id'])
        return None
    
    def get_current_hotel_owner():
        """Get current logged in hotel owner"""
        if 'hotel_owner_id' in session:
            return HotelOwner.query.get(session['hotel_owner_id'])
        return None
    
    def get_current_admin():
        """Get current logged in admin"""
        if 'admin_id' in session:
            return Admin.query.get(session['admin_id'])
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
        
        # Get hotel data with proper images
        hotels = HotelOwner.query.filter_by(is_verified=True, is_active=True, is_approved=True).all()
        hotels_data = []
        
        # Restaurant images mapping (using live restaurant images)
        restaurant_images = {
            'Hotel Sareng': 'https://images.unsplash.com/photo-1514933651103-005eec06c04b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80',
            'MasterCafe': 'https://images.unsplash.com/photo-1554118811-1e0d58224f24?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80',
            'Chondrobindu': 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80',
            'Master Cafe': 'https://images.unsplash.com/photo-1554118811-1e0d58224f24?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80',
            'chrondobindu Cafe': 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80',
            'Hall': 'https://images.unsplash.com/photo-1559339352-11d035aa65de?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80'
        }
        
        for hotel in hotels:
            hotel_data = hotel.to_dict()
            hotel_data['menu_items'] = [item.to_dict() for item in available_menu_items if item.hotel_owner_id == hotel.id]
            
            # Add template-compatible fields
            hotel_data['name'] = hotel.hotel_name
            hotel_data['address'] = hotel.hotel_address
            hotel_data['image'] = restaurant_images.get(hotel.hotel_name, 'https://images.unsplash.com/photo-1514933651103-005eec06c04b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80')
            hotel_data['cuisine_type'] = 'Bengali & Continental'
            hotel_data['price_range'] = '₹80-250'
            hotel_data['delivery_time'] = '25-35'
            
            hotels_data.append(hotel_data)
        
        # Get sample data for dynamic placeholders
        sample_food_price = 80
        sample_food_quantity = 5
        sample_menu_price = 150
        
        # Get recent prices for realistic examples
        recent_posts = StudentFoodPost.query.filter(StudentFoodPost.expires_at > datetime.utcnow()).order_by(StudentFoodPost.created_at.desc()).limit(3).all()
        recent_menu_items = MenuItem.query.filter(MenuItem.expires_at > datetime.utcnow()).order_by(MenuItem.created_at.desc()).limit(3).all()
        
        if recent_posts:
            sample_food_price = recent_posts[0].price
            sample_food_quantity = recent_posts[0].quantity
        
        if recent_menu_items:
            sample_menu_price = recent_menu_items[0].price

        return render_template('index.html', 
                             posts=all_posts,
                             all_posts=all_posts,  # Ensure all_posts is available
                             hotels=hotels_data,
                             homemade_food=recent_food_posts,  # Pass raw posts for homemade section
                             sample_food_price=sample_food_price,
                             sample_food_quantity=sample_food_quantity,
                             sample_menu_price=sample_menu_price,
                             current_user=get_current_user())

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
                email=data['email'],
                is_approved=False  # Requires admin approval
            )
            user.set_password(data['password'])
            
            db.session.add(user)
            db.session.commit()
            
            # Note: Don't automatically log in - user needs approval first
            return jsonify({
                'success': True, 
                'message': 'Registration successful. Please wait for admin approval before logging in.',
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
                is_verified=False,  # Requires manual verification
                is_approved=False   # Requires admin approval
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
                    (HotelOwner.username == username) | (HotelOwner.email == username),
                    HotelOwner.is_active == True
                ).first()
                
                if hotel_owner and hotel_owner.check_password(password):
                    if not hotel_owner.is_approved:
                        return jsonify({'success': False, 'message': 'Your account is pending admin approval'}), 401
                    
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
                    (User.username == username) | (User.email == username),
                    User.is_active == True
                ).first()
                
                if user and user.check_password(password):
                    if not user.is_approved:
                        return jsonify({'success': False, 'message': 'Your account is pending admin approval'}), 401
                    
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
    # ADMIN AUTHENTICATION ROUTES
    # ==================================================================================
    
    @app.route('/admin/login', methods=['GET', 'POST'])
    def admin_login():
        """Admin login"""
        if request.method == 'GET':
            return render_template('admin/login.html')
        
        try:
            # Handle both JSON and form data
            if request.is_json:
                data = request.get_json()
            else:
                data = request.form.to_dict()
            
            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                return jsonify({'success': False, 'message': 'Username and password are required'}), 400
            
            # Find admin by username
            admin = Admin.query.filter_by(username=username, is_active=True).first()
            
            if admin and admin.check_password(password):
                session['admin_id'] = admin.id
                
                app.logger.info(f"Admin login successful for: {username}")
                
                # For AJAX requests, return JSON
                if request.is_json or request.headers.get('Content-Type') == 'application/json':
                    return jsonify({
                        'success': True, 
                        'message': 'Login successful',
                        'redirect': '/admin/dashboard'
                    })
                
                # For regular browser requests, redirect to admin dashboard
                return redirect(url_for('admin_dashboard'))
            else:
                app.logger.warning(f"Failed admin login attempt for: {username}")
                return jsonify({'success': False, 'message': 'Invalid username or password'}), 401
        
        except Exception as e:
            app.logger.error(f"Admin login error: {str(e)}")
            return jsonify({'success': False, 'message': 'Login failed'}), 500
    
    @app.route('/admin/logout', methods=['GET', 'POST'])
    def admin_logout():
        """Admin logout"""
        if 'admin_id' in session:
            del session['admin_id']
        
        # For AJAX requests, return JSON
        if request.is_json or request.headers.get('Content-Type') == 'application/json':
            return jsonify({'success': True, 'message': 'Logged out successfully'})
        
        # For regular browser requests, redirect to admin login
        return redirect(url_for('admin_login'))

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
            
            # Broadcast new review to all users
            review_data = {
                'id': review.id,
                'user': {'name': review.user.username},
                'rating': review.rating,
                'restaurant': menu_item.hotel_owner.hotel_name,
                'menuItem': menu_item.item_name,
                'price': menu_item.price,
                'comment': review.comment,
                'image': review.image_url or '',
                'timeAgo': 'Just now',
                'type': 'review'
            }
            broadcast_new_post(review_data, 'review')
            
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
            
            # Broadcast new food post to all users
            post_data = {
                'id': food_post.id,
                'user': {'name': food_post.user.username},
                'title': food_post.title,
                'description': food_post.description,
                'price': food_post.price,
                'image': food_post.image_url or 'https://via.placeholder.com/300x200',
                'location': food_post.location,
                'isVegetarian': food_post.food_type == 'veg',
                'timeAgo': 'Just now',
                'type': 'homemade'
            }
            broadcast_new_post(post_data, 'homemade')
            
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
    
    @app.route('/delete-menu-item/<int:item_id>', methods=['DELETE'])
    def delete_menu_item(item_id):
        """Delete menu item (Hotel owners only)"""
        if not require_hotel_login():
            return jsonify({'success': False, 'message': 'Please login as hotel owner first'}), 401
        
        try:
            # Find the menu item
            menu_item = MenuItem.query.filter_by(
                id=item_id, 
                hotel_owner_id=session['hotel_owner_id']
            ).first()
            
            if not menu_item:
                return jsonify({'success': False, 'message': 'Menu item not found or not authorized'}), 404
            
            # Delete the menu item
            db.session.delete(menu_item)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Menu item deleted successfully!'
            })
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Menu item deletion error: {str(e)}")
            return jsonify({'success': False, 'message': 'Failed to delete menu item'}), 500

    @app.route('/toggle-menu-availability/<int:item_id>', methods=['PUT'])
    def toggle_menu_availability(item_id):
        """Toggle menu item availability (Hotel owners only)"""
        if not require_hotel_login():
            return jsonify({'success': False, 'message': 'Please login as hotel owner first'}), 401
        
        try:
            # Find the menu item
            menu_item = MenuItem.query.filter_by(
                id=item_id, 
                hotel_owner_id=session['hotel_owner_id']
            ).first()
            
            if not menu_item:
                return jsonify({'success': False, 'message': 'Menu item not found or not authorized'}), 404
            
            # Toggle availability
            menu_item.is_available = not menu_item.is_available
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': f'Menu item {"enabled" if menu_item.is_available else "disabled"} successfully!',
                'is_available': menu_item.is_available
            })
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Menu item toggle error: {str(e)}")
            return jsonify({'success': False, 'message': 'Failed to update menu item'}), 500

    @app.route('/cleanup-expired', methods=['POST'])
    def manual_cleanup():
        """Manually trigger cleanup of expired content (Admin/Hotel owners)"""
        if not (require_hotel_login() or require_login()):
            return jsonify({'success': False, 'message': 'Authentication required'}), 401
        
        try:
            deleted_count = cleanup_expired_content()
            return jsonify({
                'success': True,
                'message': f'Cleanup completed! Removed {deleted_count} expired items.',
                'deleted_count': deleted_count
            })
        except Exception as e:
            app.logger.error(f"Manual cleanup error: {str(e)}")
            return jsonify({'success': False, 'message': 'Cleanup failed'}), 500

    @app.route('/menu-stats', methods=['GET'])
    def menu_stats():
        """Get menu statistics for hotel owner"""
        if not require_hotel_login():
            return jsonify({'success': False, 'message': 'Please login as hotel owner first'}), 401
        
        try:
            hotel_id = session['hotel_owner_id']
            
            # Get menu item counts
            total_items = MenuItem.query.filter_by(hotel_owner_id=hotel_id).count()
            active_items = MenuItem.query.filter_by(
                hotel_owner_id=hotel_id, 
                is_available=True
            ).filter(MenuItem.expires_at > datetime.utcnow()).count()
            expired_items = MenuItem.query.filter_by(
                hotel_owner_id=hotel_id
            ).filter(MenuItem.expires_at <= datetime.utcnow()).count()
            
            # Get recent reviews
            recent_reviews = Review.query.join(MenuItem).filter(
                MenuItem.hotel_owner_id == hotel_id,
                Review.created_at >= datetime.utcnow() - timedelta(days=7)
            ).count()
            
            return jsonify({
                'success': True,
                'stats': {
                    'total_items': total_items,
                    'active_items': active_items,
                    'expired_items': expired_items,
                    'recent_reviews': recent_reviews
                }
            })
            
        except Exception as e:
            app.logger.error(f"Menu stats error: {str(e)}")
            return jsonify({'success': False, 'message': 'Failed to fetch stats'}), 500

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
    # POST INTERACTION & NOTIFICATION ROUTES
    # ==================================================================================
    
    @app.route('/api/post/like', methods=['POST'])
    def like_post():
        """Like or unlike a post"""
        try:
            user = get_current_user()
            if not user:
                return jsonify({'success': False, 'message': 'Login required'}), 401
            
            data = request.get_json()
            post_id = data.get('post_id')
            post_type = data.get('post_type')  # 'review' or 'food_post'
            
            if not post_id or not post_type:
                return jsonify({'success': False, 'message': 'Missing required fields'}), 400
            
            # Check if user already liked this post
            existing_like = PostInteraction.query.filter_by(
                user_id=user.id,
                post_id=post_id,
                post_type=post_type,
                interaction_type='like'
            ).first()
            
            if existing_like:
                # Unlike the post
                db.session.delete(existing_like)
                action = 'unliked'
            else:
                # Like the post
                like = PostInteraction(
                    user_id=user.id,
                    post_id=post_id,
                    post_type=post_type,
                    interaction_type='like'
                )
                db.session.add(like)
                action = 'liked'
                
                # Create notification for post owner (only for student users)
                if post_type == 'review':
                    post = Review.query.get(post_id)
                    if post and post.user_id != user.id:
                        # Check if the liker is a student user (has username attribute from User model)
                        liker_name = getattr(user, 'username', getattr(user, 'hotel_name', 'Someone'))
                        create_notification(
                            user_id=post.user_id,
                            notification_type='like',
                            title='New Like!',
                            message=f'{liker_name} liked your review',
                            related_id=post_id,
                            related_type='review'
                        )
                elif post_type == 'food_post':
                    post = StudentFoodPost.query.get(post_id)
                    if post and post.user_id != user.id:
                        # Check if the liker is a student user
                        liker_name = getattr(user, 'username', getattr(user, 'hotel_name', 'Someone'))
                        create_notification(
                            user_id=post.user_id,
                            notification_type='like',
                            title='New Like!',
                            message=f'{liker_name} liked your food post',
                            related_id=post_id,
                            related_type='food_post'
                        )
            
            db.session.commit()
            
            # Get updated counts
            likes_count = PostInteraction.get_post_likes_count(post_id, post_type)
            user_has_liked = PostInteraction.user_has_liked(user.id, post_id, post_type)
            
            return jsonify({
                'success': True,
                'action': action,
                'likes_count': likes_count,
                'user_has_liked': user_has_liked
            })
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error handling like: {str(e)}")
            return jsonify({'success': False, 'message': 'Failed to process like'}), 500
    
    @app.route('/api/post/comment', methods=['POST'])
    def comment_on_post():
        """Add a comment to a post"""
        try:
            user = get_current_user()
            if not user:
                return jsonify({'success': False, 'message': 'Login required'}), 401
            
            data = request.get_json()
            post_id = data.get('post_id')
            post_type = data.get('post_type')
            comment_text = data.get('comment_text', '').strip()
            
            if not post_id or not post_type or not comment_text:
                return jsonify({'success': False, 'message': 'Missing required fields'}), 400
            
            if len(comment_text) > 500:
                return jsonify({'success': False, 'message': 'Comment too long (max 500 characters)'}), 400
            
            # Create comment
            comment = PostInteraction(
                user_id=user.id,
                post_id=post_id,
                post_type=post_type,
                interaction_type='comment',
                comment_text=comment_text
            )
            db.session.add(comment)
            
            # Create notification for post owner
            if post_type == 'review':
                post = Review.query.get(post_id)
                if post and post.user_id != user.id:
                    create_notification(
                        user_id=post.user_id,
                        notification_type='comment',
                        title='New Comment!',
                        message=f'{user.username} commented on your review',
                        related_id=post_id,
                        related_type='review'
                    )
            elif post_type == 'food_post':
                post = StudentFoodPost.query.get(post_id)
                if post and post.user_id != user.id:
                    create_notification(
                        user_id=post.user_id,
                        notification_type='comment',
                        title='New Comment!',
                        message=f'{user.username} commented on your food post',
                        related_id=post_id,
                        related_type='food_post'
                    )
            
            db.session.commit()
            
            # Get updated counts
            comments_count = PostInteraction.get_post_comments_count(post_id, post_type)
            
            return jsonify({
                'success': True,
                'comment': comment.to_dict(),
                'comments_count': comments_count
            })
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error adding comment: {str(e)}")
            return jsonify({'success': False, 'message': 'Failed to add comment'}), 500
    
    @app.route('/api/notifications')
    def get_notifications():
        """Get user notifications"""
        try:
            user = get_current_user()
            if not user:
                return jsonify({'success': False, 'message': 'Login required'}), 401
            
            # Only return notifications for student users (User model)
            # Hotel owners don't have notifications yet
            if not hasattr(user, 'reg_number'):  # Hotel owners don't have reg_number
                return jsonify({
                    'success': True,
                    'notifications': [],
                    'unread_count': 0
                })
            
            notifications = Notification.query.filter_by(user_id=user.id)\
                                           .filter(Notification.expires_at > datetime.utcnow())\
                                           .order_by(Notification.created_at.desc())\
                                           .limit(50).all()
            
            unread_count = Notification.query.filter_by(user_id=user.id, is_read=False)\
                                          .filter(Notification.expires_at > datetime.utcnow())\
                                          .count()
            
            return jsonify({
                'success': True,
                'notifications': [notification.to_dict() for notification in notifications],
                'unread_count': unread_count
            })
            
        except Exception as e:
            app.logger.error(f"Error getting notifications: {str(e)}")
            return jsonify({'success': False, 'message': 'Failed to get notifications'}), 500
    
    @app.route('/api/post/interactions/<int:post_id>/<post_type>')
    def get_post_interactions(post_id, post_type):
        """Get post interaction counts and user's interaction status"""
        try:
            user = get_current_user()
            
            likes_count = PostInteraction.get_post_likes_count(post_id, post_type)
            comments_count = PostInteraction.get_post_comments_count(post_id, post_type)
            
            user_has_liked = False
            if user:
                user_has_liked = PostInteraction.user_has_liked(user.id, post_id, post_type)
            
            # Get recent comments
            comments = PostInteraction.query.filter_by(
                post_id=post_id,
                post_type=post_type,
                interaction_type='comment'
            ).order_by(PostInteraction.created_at.desc()).limit(5).all()
            
            return jsonify({
                'success': True,
                'likes_count': likes_count,
                'comments_count': comments_count,
                'user_has_liked': user_has_liked,
                'recent_comments': [comment.to_dict() for comment in comments]
            })
            
        except Exception as e:
            app.logger.error(f"Error getting post interactions: {str(e)}")
            return jsonify({'success': False, 'message': 'Failed to get interactions'}), 500

    # ==================================================================================
    # ADMIN PANEL ROUTES
    # ==================================================================================
    
    @app.route('/admin/dashboard')
    def admin_dashboard():
        """Admin dashboard"""
        if not require_admin_login():
            return redirect(url_for('admin_login'))
        
        # Get statistics
        pending_users = User.query.filter_by(is_approved=False, is_active=True).count()
        pending_hotels = HotelOwner.query.filter_by(is_approved=False, is_active=True).count()
        total_users = User.query.filter_by(is_active=True).count()
        total_hotels = HotelOwner.query.filter_by(is_active=True).count()
        total_reviews = Review.query.count()
        total_food_posts = StudentFoodPost.query.count()
        
        stats = {
            'pending_users': pending_users,
            'pending_hotels': pending_hotels,
            'total_users': total_users,
            'total_hotels': total_hotels,
            'total_reviews': total_reviews,
            'total_food_posts': total_food_posts
        }
        
        return render_template('admin/dashboard.html', stats=stats, current_admin=get_current_admin())
    
    @app.route('/admin/users')
    def admin_users():
        """Manage users"""
        if not require_admin_login():
            return redirect(url_for('admin_login'))
        
        status = request.args.get('status', 'all')
        
        if status == 'pending':
            users = User.query.filter_by(is_approved=False, is_active=True).order_by(User.created_at.desc()).all()
        elif status == 'approved':
            users = User.query.filter_by(is_approved=True, is_active=True).order_by(User.created_at.desc()).all()
        else:
            users = User.query.filter_by(is_active=True).order_by(User.created_at.desc()).all()
        
        return render_template('admin/users.html', users=users, status=status, current_admin=get_current_admin())
    
    @app.route('/admin/hotels')
    def admin_hotels():
        """Manage hotel owners"""
        if not require_admin_login():
            return redirect(url_for('admin_login'))
        
        status = request.args.get('status', 'all')
        
        if status == 'pending':
            hotels = HotelOwner.query.filter_by(is_approved=False, is_active=True).order_by(HotelOwner.created_at.desc()).all()
        elif status == 'approved':
            hotels = HotelOwner.query.filter_by(is_approved=True, is_active=True).order_by(HotelOwner.created_at.desc()).all()
        else:
            hotels = HotelOwner.query.filter_by(is_active=True).order_by(HotelOwner.created_at.desc()).all()
        
        return render_template('admin/hotels.html', hotels=hotels, status=status, current_admin=get_current_admin())
    
    @app.route('/admin/approve-user/<int:user_id>', methods=['POST'])
    def approve_user(user_id):
        """Approve a user registration"""
        if not require_admin_login():
            return jsonify({'success': False, 'message': 'Admin login required'}), 401
        
        try:
            user = User.query.get_or_404(user_id)
            admin = get_current_admin()
            
            user.is_approved = True
            user.approved_by = admin.id
            user.approved_at = datetime.utcnow()
            
            db.session.commit()
            
            app.logger.info(f"User {user.username} approved by admin {admin.username}")
            return jsonify({'success': True, 'message': f'User {user.username} approved successfully'})
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error approving user: {str(e)}")
            return jsonify({'success': False, 'message': 'Failed to approve user'}), 500
    
    @app.route('/admin/approve-hotel/<int:hotel_id>', methods=['POST'])
    def approve_hotel(hotel_id):
        """Approve a hotel owner registration"""
        if not require_admin_login():
            return jsonify({'success': False, 'message': 'Admin login required'}), 401
        
        try:
            hotel = HotelOwner.query.get_or_404(hotel_id)
            admin = get_current_admin()
            
            hotel.is_approved = True
            hotel.is_verified = True  # Also verify the hotel
            hotel.approved_by = admin.id
            hotel.approved_at = datetime.utcnow()
            
            db.session.commit()
            
            app.logger.info(f"Hotel {hotel.hotel_name} approved by admin {admin.username}")
            return jsonify({'success': True, 'message': f'Hotel {hotel.hotel_name} approved successfully'})
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error approving hotel: {str(e)}")
            return jsonify({'success': False, 'message': 'Failed to approve hotel'}), 500
    
    @app.route('/admin/delete-user/<int:user_id>', methods=['DELETE'])
    def delete_user(user_id):
        """Delete a user (soft delete)"""
        if not require_admin_login():
            return jsonify({'success': False, 'message': 'Admin login required'}), 401
        
        try:
            user = User.query.get_or_404(user_id)
            admin = get_current_admin()
            
            user.is_active = False
            db.session.commit()
            
            app.logger.info(f"User {user.username} deleted by admin {admin.username}")
            return jsonify({'success': True, 'message': f'User {user.username} deleted successfully'})
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error deleting user: {str(e)}")
            return jsonify({'success': False, 'message': 'Failed to delete user'}), 500
    
    @app.route('/admin/delete-hotel/<int:hotel_id>', methods=['DELETE'])
    def delete_hotel(hotel_id):
        """Delete a hotel owner (soft delete)"""
        if not require_admin_login():
            return jsonify({'success': False, 'message': 'Admin login required'}), 401
        
        try:
            hotel = HotelOwner.query.get_or_404(hotel_id)
            admin = get_current_admin()
            
            hotel.is_active = False
            db.session.commit()
            
            app.logger.info(f"Hotel {hotel.hotel_name} deleted by admin {admin.username}")
            return jsonify({'success': True, 'message': f'Hotel {hotel.hotel_name} deleted successfully'})
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error deleting hotel: {str(e)}")
            return jsonify({'success': False, 'message': 'Failed to delete hotel'}), 500
    
    @app.route('/admin/reviews')
    def admin_reviews():
        """Manage reviews"""
        if not require_admin_login():
            return redirect(url_for('admin_login'))
        
        reviews = Review.query.order_by(Review.created_at.desc()).all()
        return render_template('admin/reviews.html', reviews=reviews, current_admin=get_current_admin())
    
    @app.route('/admin/delete-review/<int:review_id>', methods=['DELETE'])
    def delete_review(review_id):
        """Delete a review"""
        if not require_admin_login():
            return jsonify({'success': False, 'message': 'Admin login required'}), 401
        
        try:
            review = Review.query.get_or_404(review_id)
            admin = get_current_admin()
            
            db.session.delete(review)
            db.session.commit()
            
            app.logger.info(f"Review {review_id} deleted by admin {admin.username}")
            return jsonify({'success': True, 'message': 'Review deleted successfully'})
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error deleting review: {str(e)}")
            return jsonify({'success': False, 'message': 'Failed to delete review'}), 500
    
    @app.route('/admin/food-posts')
    def admin_food_posts():
        """Manage student food posts"""
        if not require_admin_login():
            return redirect(url_for('admin_login'))
        
        food_posts = StudentFoodPost.query.order_by(StudentFoodPost.created_at.desc()).all()
        return render_template('admin/food_posts.html', 
                             food_posts=food_posts, 
                             current_admin=get_current_admin(),
                             current_time=datetime.utcnow())
    
    @app.route('/admin/delete-food-post/<int:post_id>', methods=['DELETE'])
    def delete_food_post(post_id):
        """Delete a food post"""
        if not require_admin_login():
            return jsonify({'success': False, 'message': 'Admin login required'}), 401
        
        try:
            post = StudentFoodPost.query.get_or_404(post_id)
            admin = get_current_admin()
            
            db.session.delete(post)
            db.session.commit()
            
            app.logger.info(f"Food post {post_id} deleted by admin {admin.username}")
            return jsonify({'success': True, 'message': 'Food post deleted successfully'})
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error deleting food post: {str(e)}")
            return jsonify({'success': False, 'message': 'Failed to delete food post'}), 500

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

    # ==================================================================================
    # REAL-TIME NOTIFICATION FUNCTIONS
    # ==================================================================================
    
    def create_notification(user_id, notification_type, title, message, related_id=None, related_type=None):
        """Create and emit a real-time notification"""
        try:
            notification = Notification(
                user_id=user_id,
                type=notification_type,
                title=title,
                message=message,
                related_id=related_id,
                related_type=related_type
            )
            db.session.add(notification)
            db.session.commit()
            
            # Emit real-time notification
            socketio.emit('new_notification', notification.to_dict(), room=f'user_{user_id}')
            
            return notification
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error creating notification: {str(e)}")
            return None
    
    def broadcast_new_post(post_data, post_type):
        """Broadcast new post to all connected users"""
        try:
            socketio.emit('new_post', {
                'type': post_type,
                'data': post_data,
                'timestamp': datetime.utcnow().isoformat()
            }, broadcast=True)
        except Exception as e:
            app.logger.error(f"Error broadcasting new post: {str(e)}")
    
    # ==================================================================================
    # WEBSOCKET EVENTS
    # ==================================================================================
    
    @socketio.on('connect')
    def handle_connect():
        """Handle user connection"""
        try:
            user = get_current_user()
            if user:
                join_room(f'user_{user.id}')
                emit('connected', {'status': 'Connected successfully'})
                app.logger.info(f"User {user.username} connected to notifications")
        except Exception as e:
            app.logger.error(f"Connection error: {str(e)}")
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle user disconnection"""
        try:
            user = get_current_user()
            if user:
                leave_room(f'user_{user.id}')
                app.logger.info(f"User {user.username} disconnected from notifications")
        except Exception as e:
            app.logger.error(f"Disconnection error: {str(e)}")
    
    @socketio.on('mark_notification_read')
    def handle_mark_notification_read(data):
        """Mark notification as read"""
        try:
            user = get_current_user()
            if not user:
                return
            
            notification_id = data.get('notification_id')
            notification = Notification.query.filter_by(id=notification_id, user_id=user.id).first()
            
            if notification:
                notification.is_read = True
                db.session.commit()
                emit('notification_marked_read', {'notification_id': notification_id})
        except Exception as e:
            app.logger.error(f"Error marking notification as read: {str(e)}")
    
    # Store functions in app for use in routes
    app.create_notification = create_notification
    app.broadcast_new_post = broadcast_new_post

    return app

# Create the app instance
app = create_app()

# Background cleanup scheduler
def run_cleanup_scheduler():
    """Run periodic cleanup of expired content"""
    import time
    import threading
    
    def cleanup_worker():
        while True:
            try:
                with app.app_context():
                    deleted_count = cleanup_expired_content()
                    if deleted_count > 0:
                        app.logger.info(f"Cleaned up {deleted_count} expired items")
                # Run cleanup every 30 minutes
                time.sleep(1800)
            except Exception as e:
                app.logger.error(f"Cleanup error: {str(e)}")
                time.sleep(300)  # Wait 5 minutes before retrying
    
    # Start cleanup thread
    cleanup_thread = threading.Thread(target=cleanup_worker, daemon=True)
    cleanup_thread.start()
    app.logger.info("Started background cleanup scheduler")

# Start the cleanup scheduler
run_cleanup_scheduler()

if __name__ == '__main__':
    # Use environment variable for debug mode, default to False for production
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
