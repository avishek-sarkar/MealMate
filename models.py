"""
Database models for MealMate Campus Food Hub
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Admin(db.Model):
    """Admin user model"""
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    is_super_admin = db.Column(db.Boolean, default=False)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert admin to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'is_active': self.is_active,
            'is_super_admin': self.is_super_admin
        }
    
    def __repr__(self):
        return f'<Admin {self.username}>'

class User(db.Model):
    """Student user model"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    reg_number = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    is_approved = db.Column(db.Boolean, default=False)  # Admin approval required
    approved_by = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=True)
    approved_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    reviews = db.relationship('Review', backref='user', lazy=True, cascade='all, delete-orphan')
    food_posts = db.relationship('StudentFoodPost', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'reg_number': self.reg_number,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'is_active': self.is_active,
            'is_approved': self.is_approved,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None
        }
    
    def __repr__(self):
        return f'<User {self.username}>'


class HotelOwner(db.Model):
    """Hotel owner model"""
    __tablename__ = 'hotel_owners'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    hotel_name = db.Column(db.String(100), nullable=False)
    hotel_address = db.Column(db.Text, nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)
    license_number = db.Column(db.String(50), nullable=True)
    is_verified = db.Column(db.Boolean, default=False)
    is_approved = db.Column(db.Boolean, default=False)  # Admin approval required
    approved_by = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=True)
    approved_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    menu_items = db.relationship('MenuItem', backref='hotel_owner', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert hotel owner to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'hotel_name': self.hotel_name,
            'hotel_address': self.hotel_address,
            'contact_number': self.contact_number,
            'is_verified': self.is_verified,
            'is_approved': self.is_approved,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<HotelOwner {self.hotel_name}>'


class MenuItem(db.Model):
    """Hotel menu items model"""
    __tablename__ = 'menu_items'
    
    id = db.Column(db.Integer, primary_key=True)
    hotel_owner_id = db.Column(db.Integer, db.ForeignKey('hotel_owners.id'), nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # breakfast, lunch, dinner, snacks
    image_url = db.Column(db.String(255), nullable=True)
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(hours=24))
    
    # Relationships
    reviews = db.relationship('Review', backref='menu_item', lazy=True, cascade='all, delete-orphan')
    
    @property
    def is_expired(self):
        """Check if menu item has expired (24 hour rule)"""
        return datetime.utcnow() > self.expires_at
    
    @property
    def time_remaining(self):
        """Get time remaining before expiry"""
        if self.is_expired:
            return timedelta(0)
        return self.expires_at - datetime.utcnow()
    
    @property
    def average_rating(self):
        """Calculate average rating from reviews"""
        if not self.reviews:
            return 0
        return sum(review.rating for review in self.reviews) / len(self.reviews)
    
    def to_dict(self):
        """Convert menu item to dictionary"""
        return {
            'id': self.id,
            'hotel_owner_id': self.hotel_owner_id,
            'hotel_name': self.hotel_owner.hotel_name,
            'item_name': self.item_name,
            'description': self.description,
            'price': self.price,
            'category': self.category,
            'image_url': self.image_url,
            'is_available': self.is_available,
            'is_expired': self.is_expired,
            'time_remaining': str(self.time_remaining),
            'average_rating': round(self.average_rating, 1),
            'review_count': len(self.reviews),
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat()
        }
    
    def __repr__(self):
        return f'<MenuItem {self.item_name}>'


class Review(db.Model):
    """Reviews model for menu items"""
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(hours=24))
    
    # Add constraints
    __table_args__ = (
        db.CheckConstraint('rating >= 1 AND rating <= 5', name='valid_rating'),
        db.UniqueConstraint('user_id', 'menu_item_id', name='unique_user_review'),
    )
    
    @property
    def is_expired(self):
        """Check if review has expired (24 hour rule)"""
        return datetime.utcnow() > self.expires_at
    
    @property
    def time_remaining(self):
        """Get time remaining before expiry"""
        if self.is_expired:
            return timedelta(0)
        return self.expires_at - datetime.utcnow()
    
    def to_dict(self):
        """Convert review to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.user.username,
            'menu_item_id': self.menu_item_id,
            'item_name': self.menu_item.item_name,
            'hotel_name': self.menu_item.hotel_owner.hotel_name,
            'rating': self.rating,
            'comment': self.comment,
            'image_url': self.image_url,
            'is_expired': self.is_expired,
            'time_remaining': str(self.time_remaining),
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Review {self.id} - {self.rating} stars>'


class StudentFoodPost(db.Model):
    """Student homemade food posts model"""
    __tablename__ = 'student_food_posts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    food_type = db.Column(db.String(50), nullable=False)  # veg, non-veg, vegan
    cuisine = db.Column(db.String(50), nullable=True)  # indian, chinese, italian, etc.
    location = db.Column(db.String(100), nullable=False)  # hostel block, room number
    contact_info = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(hours=24))
    
    @property
    def is_expired(self):
        """Check if food post has expired (24 hour rule)"""
        return datetime.utcnow() > self.expires_at
    
    @property
    def time_remaining(self):
        """Get time remaining before expiry"""
        if self.is_expired:
            return timedelta(0)
        return self.expires_at - datetime.utcnow()
    
    def to_dict(self):
        """Convert food post to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.user.username,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'quantity': self.quantity,
            'food_type': self.food_type,
            'cuisine': self.cuisine,
            'location': self.location,
            'contact_info': self.contact_info,
            'image_url': self.image_url,
            'is_available': self.is_available,
            'is_expired': self.is_expired,
            'time_remaining': str(self.time_remaining),
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat()
        }
    
    def __repr__(self):
        return f'<StudentFoodPost {self.title}>'


# Database cleanup function
def cleanup_expired_content():
    """Remove expired reviews and food posts"""
    from datetime import datetime
    deleted_count = 0
    
    # Remove expired reviews
    expired_reviews = Review.query.filter(Review.expires_at < datetime.utcnow()).all()
    for review in expired_reviews:
        db.session.delete(review)
        deleted_count += 1
    
    # Remove expired student food posts
    expired_posts = StudentFoodPost.query.filter(StudentFoodPost.expires_at < datetime.utcnow()).all()
    for post in expired_posts:
        db.session.delete(post)
        deleted_count += 1
    
    # Remove expired menu items
    expired_items = MenuItem.query.filter(MenuItem.expires_at < datetime.utcnow()).all()
    for item in expired_items:
        db.session.delete(item)
        deleted_count += 1
    
    db.session.commit()
    return deleted_count


class Notification(db.Model):
    """Real-time notification model"""
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # 'new_post', 'like', 'comment'
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    related_id = db.Column(db.Integer, nullable=True)  # ID of related post/review
    related_type = db.Column(db.String(50), nullable=True)  # 'review', 'food_post'
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(days=7))
    
    # Relationships
    user = db.relationship('User', backref=db.backref('notifications', lazy=True))
    
    @property
    def is_expired(self):
        """Check if notification is expired"""
        return datetime.utcnow() > self.expires_at
    
    def to_dict(self):
        """Convert notification to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'type': self.type,
            'title': self.title,
            'message': self.message,
            'related_id': self.related_id,
            'related_type': self.related_type,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat(),
            'time_ago': self.get_time_ago()
        }
    
    def get_time_ago(self):
        """Get human readable time ago"""
        now = datetime.utcnow()
        diff = now - self.created_at
        
        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds >= 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds >= 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "Just now"
    
    def __repr__(self):
        return f'<Notification {self.title}>'


class PostInteraction(db.Model):
    """Model to track likes and comments on posts"""
    __tablename__ = 'post_interactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, nullable=False)
    post_type = db.Column(db.String(50), nullable=False)  # 'review', 'food_post'
    interaction_type = db.Column(db.String(20), nullable=False)  # 'like', 'comment'
    comment_text = db.Column(db.Text, nullable=True)  # Only for comments
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('post_interactions', lazy=True))
    
    @classmethod
    def get_post_likes_count(cls, post_id, post_type):
        """Get total likes for a post"""
        return cls.query.filter_by(
            post_id=post_id, 
            post_type=post_type, 
            interaction_type='like'
        ).count()
    
    @classmethod
    def get_post_comments_count(cls, post_id, post_type):
        """Get total comments for a post"""
        return cls.query.filter_by(
            post_id=post_id, 
            post_type=post_type, 
            interaction_type='comment'
        ).count()
    
    @classmethod
    def user_has_liked(cls, user_id, post_id, post_type):
        """Check if user has liked a post"""
        return cls.query.filter_by(
            user_id=user_id,
            post_id=post_id,
            post_type=post_type,
            interaction_type='like'
        ).first() is not None
    
    def to_dict(self):
        """Convert interaction to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.user.username,
            'post_id': self.post_id,
            'post_type': self.post_type,
            'interaction_type': self.interaction_type,
            'comment_text': self.comment_text,
            'created_at': self.created_at.isoformat(),
            'time_ago': self.get_time_ago()
        }
    
    def get_time_ago(self):
        """Get human readable time ago"""
        now = datetime.utcnow()
        diff = now - self.created_at
        
        if diff.days > 0:
            return f"{diff.days}d"
        elif diff.seconds >= 3600:
            hours = diff.seconds // 3600
            return f"{hours}h"
        elif diff.seconds >= 60:
            minutes = diff.seconds // 60
            return f"{minutes}m"
        else:
            return "now"
    
    def __repr__(self):
        return f'<PostInteraction {self.interaction_type} by {self.user.username}>'
