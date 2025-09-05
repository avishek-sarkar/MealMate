"""
MealMate - Campus Food Hub
A Flask web application for connecting students with local food providers.
"""

from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from flask_cors import CORS
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask application
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
CORS(app)

# ============================================================================
# MOCK DATA - Replace with database in production
# ============================================================================

USERS = [
    {
        'id': '1', 
        'name': 'Sarah Chen', 
        'email': 'sarah@student.com', 
        'avatar': 'https://via.placeholder.com/40x40'
    },
    {
        'id': '2', 
        'name': 'Raj Patel', 
        'email': 'raj@student.com', 
        'avatar': 'https://via.placeholder.com/40x40'
    },
    {
        'id': '3', 
        'name': 'Priya Sharma', 
        'email': 'priya@student.com', 
        'avatar': 'https://via.placeholder.com/40x40'
    },
    {
        'id': '4', 
        'name': 'Fatima Khan', 
        'email': 'fatima@student.com', 
        'avatar': 'https://via.placeholder.com/40x40'
    },
    {
        'id': '5', 
        'name': 'Maria D\'Souza', 
        'email': 'maria@student.com', 
        'avatar': 'https://via.placeholder.com/40x40'
    }
]

POSTS = [
    {
        'id': '1',
        'type': 'review',
        'user': {'id': '1', 'name': 'Sarah Chen', 'avatar': 'https://via.placeholder.com/40x40'},
        'rating': 4.5,
        'restaurant': 'Campus Cafe',
        'menuItem': 'Chicken Biryani',
        'price': 120,
        'comment': 'Just had the chicken biryani from Campus Cafe and it\'s absolutely delicious! Perfect portion size and great value for money.',
        'image': 'https://via.placeholder.com/600x300',
        'likes': 24,
        'comments': 8,
        'timeAgo': '2 hours ago',
        'expiresIn': '18 hours',
        'created_at': datetime.now() - timedelta(hours=2)
    },
    {
        'id': '2',
        'type': 'homemade',
        'user': {'id': '2', 'name': 'Raj Patel', 'avatar': 'https://via.placeholder.com/40x40'},
        'title': 'Authentic Gujarati Thali',
        'description': 'Complete thali with dal, sabzi, rotis, rice, and sweet. Made with love by my mom!',
        'price': 80,
        'image': 'https://via.placeholder.com/600x300',
        'location': 'Hostel Block C',
        'isVegetarian': True,
        'servingSize': 1,
        'likes': 15,
        'comments': 5,
        'timeAgo': '4 hours ago',
        'expiresIn': '14 hours',
        'created_at': datetime.now() - timedelta(hours=4)
    },
    {
        'id': '3',
        'type': 'review',
        'user': {'id': '3', 'name': 'Priya Sharma', 'avatar': 'https://via.placeholder.com/40x40'},
        'rating': 3.0,
        'restaurant': 'Spice Junction',
        'menuItem': 'Paneer Tikka',
        'price': 150,
        'comment': 'The paneer tikka was okay. The portion was good but it was a bit too spicy for my taste.',
        'likes': 8,
        'comments': 3,
        'timeAgo': '6 hours ago',
        'expiresIn': '12 hours',
        'created_at': datetime.now() - timedelta(hours=6)
    }
]

HOTELS = [
    {
        'id': '1',
        'name': 'Campus Cafe',
        'description': 'Traditional Indian cuisine with modern twist',
        'location': 'Near Main Gate',
        'rating': 4.2,
        'openTime': '8:00 AM',
        'closeTime': '10:00 PM',
        'image': 'https://via.placeholder.com/300x150',
        'menu': [
            {'name': 'Chicken Biryani', 'price': 120},
            {'name': 'Veg Thali', 'price': 80},
            {'name': 'Masala Dosa', 'price': 60}
        ]
    },
    {
        'id': '2',
        'name': 'Spice Junction',
        'description': 'North Indian specialties and Chinese fusion',
        'location': 'Food Court',
        'rating': 3.8,
        'openTime': '10:00 AM',
        'closeTime': '11:00 PM',
        'image': 'https://via.placeholder.com/300x150',
        'menu': [
            {'name': 'Paneer Tikka', 'price': 150},
            {'name': 'Chicken Fried Rice', 'price': 100},
            {'name': 'Veg Noodles', 'price': 80}
        ]
    },
    {
        'id': '3',
        'name': 'Quick Bites',
        'description': 'Fast food and healthy snacks',
        'location': 'Library Block',
        'rating': 4.0,
        'openTime': '7:00 AM',
        'closeTime': '9:00 PM',
        'image': 'https://via.placeholder.com/300x150',
        'menu': [
            {'name': 'Club Sandwich', 'price': 90},
            {'name': 'Fresh Fruit Bowl', 'price': 50},
            {'name': 'Cold Coffee', 'price': 40}
        ]
    }
]

HOMEMADE_FOOD = [
    {
        'id': '1',
        'seller': {'id': '2', 'name': 'Raj Patel', 'avatar': 'https://via.placeholder.com/30x30'},
        'title': 'Authentic Gujarati Thali',
        'description': 'Complete thali with dal, sabzi, rotis, rice, and sweet',
        'price': 80,
        'image': 'https://via.placeholder.com/250x200',
        'location': 'Block C',
        'isVegetarian': True,
        'servingSize': 1,
        'expiresIn': '14h left',
        'created_at': datetime.now() - timedelta(hours=10)
    },
    {
        'id': '2',
        'seller': {'id': '4', 'name': 'Fatima Khan', 'avatar': 'https://via.placeholder.com/30x30'},
        'title': 'Mom\'s Special Biryani',
        'description': 'Hyderabadi style chicken biryani with raita and shorba',
        'price': 200,
        'image': 'https://via.placeholder.com/250x200',
        'location': 'Block A',
        'isVegetarian': False,
        'servingSize': 2,
        'expiresIn': '8h left',
        'created_at': datetime.now() - timedelta(hours=16)
    },
    {
        'id': '3',
        'seller': {'id': '5', 'name': 'Maria D\'Souza', 'avatar': 'https://via.placeholder.com/30x30'},
        'title': 'Fresh Pasta & Garlic Bread',
        'description': 'Creamy white sauce pasta with homemade garlic bread',
        'price': 120,
        'image': 'https://via.placeholder.com/250x200',
        'location': 'Block B',
        'isVegetarian': True,
        'servingSize': 1,
        'expiresIn': '20h left',
        'created_at': datetime.now() - timedelta(hours=4)
    }
]

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def calculate_time_remaining(created_at):
    """
    Calculate time remaining until 24-hour expiry.
    
    Args:
        created_at (datetime): When the content was created
        
    Returns:
        str: Human-readable time remaining
    """
    expires_at = created_at + timedelta(hours=24)
    remaining = expires_at - datetime.now()
    
    if remaining.total_seconds() <= 0:
        return "Expired"
    
    hours = int(remaining.total_seconds() // 3600)
    if hours <= 0:
        minutes = int((remaining.total_seconds() % 3600) // 60)
        return f"{minutes}m left"
    
    return f"{hours}h left"


def get_time_ago(created_at):
    """
    Get human-readable time ago string.
    
    Args:
        created_at (datetime): When the content was created
        
    Returns:
        str: Human-readable time ago
    """
    diff = datetime.now() - created_at
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


def filter_expired_content():
    """Remove content older than 24 hours."""
    current_time = datetime.now()
    
    global POSTS, HOMEMADE_FOOD
    POSTS = [post for post in POSTS if (current_time - post['created_at']).total_seconds() < 86400]
    HOMEMADE_FOOD = [food for food in HOMEMADE_FOOD if (current_time - food['created_at']).total_seconds() < 86400]


def find_user_by_email(email):
    """Find user by email address."""
    return next((user for user in USERS if user['email'] == email), None)


def find_post_by_id(post_id):
    """Find post by ID."""
    return next((post for post in POSTS if post['id'] == post_id), None)


# ============================================================================
# ROUTES
# ============================================================================
@app.route('/')
def index():
    """Main page with newsfeed."""
    filter_expired_content()
    
    # Update time-related fields
    for post in POSTS:
        post['timeAgo'] = get_time_ago(post['created_at'])
        post['expiresIn'] = calculate_time_remaining(post['created_at'])
    
    for food in HOMEMADE_FOOD:
        food['expiresIn'] = calculate_time_remaining(food['created_at'])
    
    return render_template('index.html', 
                         posts=POSTS, 
                         hotels=HOTELS, 
                         homemade_food=HOMEMADE_FOOD,
                         current_user=session.get('user'))


# ============================================================================
# AUTHENTICATION ROUTES
# ============================================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        if not email or not password:
            return jsonify({'success': False, 'error': 'Email and password required'}), 400
        
        user = find_user_by_email(email)
        
        if user:
            session['user'] = user
            return redirect(url_for('index'))
        else:
            return render_template('index.html', error='Invalid credentials')
    
    return redirect(url_for('index'))


@app.route('/register', methods=['POST'])
def register():
    """Handle user registration."""
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    
    if not all([name, email, password]):
        return jsonify({'success': False, 'error': 'All fields required'}), 400
    
    if find_user_by_email(email):
        return jsonify({'success': False, 'error': 'Email already registered'}), 400
    
    new_user = {
        'id': str(len(USERS) + 1),
        'name': name,
        'email': email,
        'avatar': 'https://via.placeholder.com/40x40'
    }
    
    USERS.append(new_user)
    session['user'] = new_user
    
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    """Handle user logout."""
    session.pop('user', None)
    return redirect(url_for('index'))

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.route('/api/posts')
def api_posts():
    """API endpoint for posts with optional filtering."""
    filter_expired_content()
    
    post_type = request.args.get('type', 'all')
    filtered_posts = POSTS if post_type == 'all' else [post for post in POSTS if post['type'] == post_type]
    
    # Update time fields
    for post in filtered_posts:
        post['timeAgo'] = get_time_ago(post['created_at'])
        post['expiresIn'] = calculate_time_remaining(post['created_at'])
    
    return jsonify(filtered_posts)


@app.route('/api/hotels')
def api_hotels():
    """API endpoint for hotels."""
    return jsonify(HOTELS)


@app.route('/api/homemade-food')
def api_homemade_food():
    """API endpoint for homemade food with sorting."""
    filter_expired_content()
    
    sort_by = request.args.get('sort', 'latest')
    
    # Update time fields
    for food in HOMEMADE_FOOD:
        food['expiresIn'] = calculate_time_remaining(food['created_at'])
    
    # Sort based on parameter
    if sort_by == 'price-low':
        HOMEMADE_FOOD.sort(key=lambda x: x['price'])
    elif sort_by == 'price-high':
        HOMEMADE_FOOD.sort(key=lambda x: x['price'], reverse=True)
    elif sort_by == 'location':
        HOMEMADE_FOOD.sort(key=lambda x: x['location'])
    
    return jsonify(HOMEMADE_FOOD)


@app.route('/api/posts/<post_id>/like', methods=['POST'])
def like_post(post_id):
    """Like/unlike a post."""
    if 'user' not in session:
        return jsonify({'success': False, 'error': 'Authentication required'}), 401
    
    post = find_post_by_id(post_id)
    if not post:
        return jsonify({'success': False, 'error': 'Post not found'}), 404
    
    # Toggle like (in production, track which users liked which posts)
    action = request.json.get('action', 'like') if request.json else 'like'
    if action == 'like':
        post['likes'] = post.get('likes', 0) + 1
    else:
        post['likes'] = max(0, post.get('likes', 0) - 1)
    
    return jsonify({'success': True, 'likes': post['likes']})


@app.route('/api/posts', methods=['POST'])
def create_post():
    """Create a new post."""
    if 'user' not in session:
        return jsonify({'success': False, 'error': 'Authentication required'}), 401
    
    if not request.json:
        return jsonify({'success': False, 'error': 'JSON data required'}), 400
    
    user = session['user']
    post_type = request.json.get('type')
    
    if post_type not in ['review', 'homemade']:
        return jsonify({'success': False, 'error': 'Invalid post type'}), 400
    
    new_post = {
        'id': str(len(POSTS) + 1),
        'type': post_type,
        'user': user,
        'likes': 0,
        'comments': 0,
        'created_at': datetime.now()
    }
    
    if post_type == 'review':
        required_fields = ['rating', 'restaurant', 'menuItem', 'price', 'comment']
        if not all(field in request.json for field in required_fields):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
            
        new_post.update({
            'rating': float(request.json.get('rating')),
            'restaurant': request.json.get('restaurant'),
            'menuItem': request.json.get('menuItem'),
            'price': int(request.json.get('price')),
            'comment': request.json.get('comment'),
            'image': request.json.get('image', '')
        })
        
    elif post_type == 'homemade':
        required_fields = ['title', 'description', 'price', 'location']
        if not all(field in request.json for field in required_fields):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
            
        new_post.update({
            'title': request.json.get('title'),
            'description': request.json.get('description'),
            'price': int(request.json.get('price')),
            'image': request.json.get('image', ''),
            'location': request.json.get('location'),
            'isVegetarian': request.json.get('isVegetarian', False),
            'servingSize': int(request.json.get('servingSize', 1))
        })
        
        # Also add to homemade food list
        HOMEMADE_FOOD.append({
            'id': new_post['id'],
            'seller': user,
            'title': new_post['title'],
            'description': new_post['description'],
            'price': new_post['price'],
            'image': new_post['image'],
            'location': new_post['location'],
            'isVegetarian': new_post['isVegetarian'],
            'servingSize': new_post['servingSize'],
            'created_at': new_post['created_at']
        })
    
    POSTS.insert(0, new_post)  # Add to beginning of list
    return jsonify({'success': True, 'post': new_post})


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_template('index.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500


# ============================================================================
# APPLICATION RUNNER
# ============================================================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
