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

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
