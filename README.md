# MealMate - Trishal Campus Food Hub 🍔

A modern Flask-based web application with real-time notifications for students in Trishal Campus, Mymensingh to share food reviews, discover local restaurants, and connect with homemade food sellers.

## 🚀 Features

### Core Features
- **Food Reviews & Posts**: Share experiences with local restaurants and dishes
- **Hotel Discovery**: Browse and discover restaurants near Trishal Campus  
- **Homemade Food Marketplace**: Connect with fellow students selling homemade food
- **Hotel Owner Dashboard**: Restaurant owners can manage menu items and track sales
- **User Authentication**: Secure login system for students and hotel owners
- **Admin Panel**: Complete admin system for user and content management

### 🔔 Real-time Features (NEW!)
- **Live Notifications**: Instant notifications for new posts, likes, and comments
- **Real-time Post Interactions**: Like and comment on posts with live updates
- **Socket.IO Integration**: WebSocket-powered real-time communication
- **Notification Bell**: Animated notification center with unread count
- **Live Broadcasting**: New posts appear instantly across all users
- **Comment System**: Real-time commenting with character limits

### Advanced Features
- **Content Expiry System**: 24-hour automatic content expiry for freshness
- **Responsive Design**: Mobile-friendly interface optimized for campus use
- **Database Integration**: SQLite with Flask-SQLAlchemy ORM
- **API Endpoints**: RESTful APIs for all major functionalities
- **Bangladeshi Context**: Prices in Taka (৳), local cuisine, and campus-specific features

## 🏫 Campus Information

- **Location**: Trishal Campus, Mymensingh, Dhaka, Bangladesh
- **Currency**: Bangladeshi Taka (৳)
- **Target Users**: Students and local restaurant owners
- **Local Cuisine**: Traditional Bangladeshi dishes including biryani, fish curry, pitha, and more

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask 3.1.2 (Python)
- **Database**: SQLite with Flask-SQLAlchemy ORM
- **Real-time**: Flask-SocketIO for WebSocket communication
- **Authentication**: Flask-Bcrypt for secure password hashing
- **Migrations**: Flask-Migrate for database version control

### Frontend
- **Templates**: Jinja2 templating engine
- **Styling**: CSS3 with responsive design and animations
- **JavaScript**: Vanilla JavaScript with Socket.IO client
- **Real-time UI**: Live notification system and interactive components

### Infrastructure
- **Environment**: Python virtual environment
- **Configuration**: python-dotenv for environment variables
- **CORS**: Flask-CORS for API endpoint support

## 📁 Project Structure

```
MealMate/
├── app.py                      # Main Flask application with Socket.IO
├── models.py                   # Database models and relationships
├── run.py                      # Application runner with environment support
├── init_db.py                  # Database initialization with sample data
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── README.md                  # Project documentation
├── REAL_TIME_NOTIFICATIONS.md # Real-time features documentation
├── migrations/                # Database migration files
├── instance/                  # Instance-specific files
├── templates/                 # Jinja2 templates
│   └── index.html            # Main application template with real-time UI
└── static/                   # Static assets
    ├── css/
    │   └── styles.css        # Enhanced styles with notification components
    └── js/
        └── script.js         # Frontend JavaScript with real-time features
```

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Step-by-step Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/avishek-sarkar/MealMate.git
   cd MealMate
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment setup**
   ```bash
   # Windows
   copy .env.example .env
   
   # Linux/Mac
   cp .env.example .env
   
   # Edit .env with your configuration
   ```

5. **Initialize database**
   ```bash
   python init_db.py
   ```

6. **Run the application**
   ```bash
   python run.py
   # or
   python app.py
   ```

7. **Access the application**
   Open your browser and navigate to `http://127.0.0.1:5000`

## 🎯 Default Login Credentials

After running `init_db.py`, you can use these credentials:

### Admin
- **Username**: admin
- **Password**: admin123

### Students
- **Username**: avishek_sarkar / tamim5 / mridula
- **Password**: password123

### Hotel Owners
- **Username**: hotel_sareng / mastercafe / chondrobindu  
- **Password**: hotel123

> **Note**: Most users and hotels require admin approval before they can fully use the system.

## 🌟 Key Features Detailed

### Real-time Notification System
- **Live Notifications**: Instant alerts for likes, comments, and new posts
- **WebSocket Integration**: Socket.IO for real-time bidirectional communication
- **User Rooms**: Personalized notification delivery
- **Notification Bell**: Animated UI component with unread count
- **Toast Messages**: Non-intrusive popup notifications

### Authentication & Authorization
- **Multi-role System**: Students, Hotel Owners, and Admins
- **Secure Sessions**: Flask session management
- **Password Hashing**: Bcrypt for secure password storage
- **Admin Approval**: User approval workflow for security

### Content Management
- **24-hour Expiry**: Automatic content cleanup for freshness
- **Real-time Updates**: Live content updates across all users
- **Image Support**: Upload and display food images
- **Rich Interactions**: Like, comment, and share functionality

### Database Architecture
- **SQLAlchemy ORM**: Modern database interactions
- **Relationship Management**: Foreign keys and relationships
- **Migration Support**: Database versioning with Flask-Migrate
- **Data Integrity**: Proper constraints and validations

## 🔒 Security Features

- **Environment Variables**: Sensitive data protection
- **CSRF Protection**: Cross-site request forgery prevention
- **Input Validation**: Server-side validation for all inputs
- **Secure Sessions**: Flask session security
- **Password Security**: Bcrypt hashing with salt
- **SQL Injection Prevention**: ORM-based database queries

## 📚 API Documentation

### Authentication Endpoints
- `POST /login` - User authentication
- `POST /logout` - User logout
- `POST /register` - User registration

### Real-time API Endpoints
- `GET /api/notifications` - Get user notifications
- `POST /api/post/like` - Like/unlike posts
- `POST /api/post/comment` - Add comments to posts
- `GET /api/post/interactions/<id>/<type>` - Get interaction counts

### Content API Endpoints
- `GET /api/posts` - Get all posts
- `GET /api/hotels` - Get hotel information
- `GET /api/homemade-food` - Get homemade food listings

## 🧪 Testing

The application includes comprehensive testing capabilities:

- **Database Testing**: Model relationships and data integrity
- **API Testing**: Endpoint functionality and security
- **Real-time Testing**: WebSocket communication and notifications
- **Authentication Testing**: Login/logout and session management

## 🚀 Development

### Code Standards
- **PEP 8**: Python coding standards compliance
- **Documentation**: Comprehensive code documentation
- **Error Handling**: Robust error handling and logging
- **Modular Design**: Separated concerns and clean architecture

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Make your changes with proper testing
4. Update documentation as needed
5. Submit a pull request

## 🔮 Future Enhancements

### Planned Features
- **Mobile App**: React Native mobile application
- **Payment Integration**: bKash/Nagad payment gateway
- **Advanced Search**: AI-powered food recommendations
- **Delivery System**: Campus delivery tracking
- **Rating Analytics**: Advanced rating and review analytics
- **Multi-language**: Bengali language support

### Technical Improvements
- **PostgreSQL**: Production database migration
- **Redis**: Caching and session storage
- **Docker**: Containerization for deployment
- **CI/CD**: Automated testing and deployment
- **Monitoring**: Application performance monitoring

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines and feel free to submit issues or pull requests.

## 📞 Support

For questions or support:
- Open an issue on GitHub
- Contact the development team
- Check the documentation in `REAL_TIME_NOTIFICATIONS.md`

---

**MealMate** - Connecting food lovers with real-time experiences, one meal at a time! 🍽️✨

*Made with ❤️ for Trishal Campus students*
