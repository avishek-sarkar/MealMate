<div align="center">

# 🍜 MealMate - Trishal Campus Food Hub 🍔

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=28&duration=3000&pause=1000&color=FF6B35&center=true&vCenter=true&width=600&lines=Connecting+Food+Lovers+%F0%9F%8D%95;Real-time+Reviews+%E2%9C%A8;Campus+Food+Community+%F0%9F%8E%93" alt="Typing SVG" />
</p>

[![Flask](https://img.shields.io/badge/Flask-3.1.2-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Socket.IO](https://img.shields.io/badge/Socket.IO-5.5.1-010101?style=for-the-badge&logo=socket.io&logoColor=white)](https://socket.io/)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

<p align="center">
  <strong>A modern Flask-based web application with real-time notifications for students in Trishal Campus, Mymensingh to share food reviews, discover local restaurants, and connect with homemade food sellers.</strong>
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-installation--setup">Installation</a> •
  <a href="#-default-login-credentials">Login</a> •
  <a href="#-technology-stack">Tech Stack</a> •
  <a href="#-api-documentation">API Docs</a>
</p>

</div>

---

## ✨ Features

<div align="center">

| 🎯 Core Features | 🔔 Real-time Features | 🔐 Advanced Features |
|:---:|:---:|:---:|
| Food Reviews & Posts | Live Notifications | Content Expiry System |
| Hotel Discovery | Real-time Interactions | Responsive Design |
| Homemade Food Marketplace | Socket.IO Integration | Database Integration |
| Hotel Owner Dashboard | Notification Bell | RESTful APIs |
| User Authentication | Live Broadcasting | Bangladeshi Context |
| Admin Panel | Comment System | Security Features |

</div>

### 🎯 Core Features
- **🍽️ Food Reviews & Posts**: Share experiences with local restaurants and dishes
- **🏨 Hotel Discovery**: Browse and discover restaurants near Trishal Campus  
- **🍱 Homemade Food Marketplace**: Connect with fellow students selling homemade food
- **📊 Hotel Owner Dashboard**: Restaurant owners can manage menu items and track sales
- **🔐 User Authentication**: Secure login system for students and hotel owners
- **👨‍💼 Admin Panel**: Complete admin system for user and content management

### 🔔 Real-time Features
- **⚡ Live Notifications**: Instant notifications for new posts, likes, and comments
- **💬 Real-time Post Interactions**: Like and comment on posts with live updates
- **🔌 Socket.IO Integration**: WebSocket-powered real-time communication
- **🔔 Notification Bell**: Animated notification center with unread count
- **📡 Live Broadcasting**: New posts appear instantly across all users
- **💭 Comment System**: Real-time commenting with character limits

### 🛡️ Advanced Features
- **⏰ Content Expiry System**: 24-hour automatic content expiry for freshness
- **📱 Responsive Design**: Mobile-friendly interface optimized for campus use
- **🗄️ Database Integration**: SQLite with Flask-SQLAlchemy ORM
- **🔗 API Endpoints**: RESTful APIs for all major functionalities
- **🇧🇩 Bangladeshi Context**: Prices in Taka (৳), local cuisine, and campus-specific features

---

## 🏫 Campus Information

<div align="center">

| 📍 Location | 💰 Currency | 👥 Target Users | 🍛 Cuisine |
|:---:|:---:|:---:|:---:|
| Trishal Campus | Bangladeshi Taka (৳) | Students & Owners | Traditional Bangladeshi |
| Mymensingh, Bangladesh | - | Campus Community | Biryani, Fish Curry, etc. |

</div>

---

## 🛠️ Technology Stack

<div align="center">

### Backend Technologies
![Flask](https://img.shields.io/badge/Flask-3.1.2-black?style=flat-square&logo=flask)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.43-red?style=flat-square)
![Flask-SocketIO](https://img.shields.io/badge/SocketIO-5.5.1-white?style=flat-square&logo=socket.io)
![Flask-Bcrypt](https://img.shields.io/badge/Bcrypt-1.0.1-yellow?style=flat-square)
![Flask-Migrate](https://img.shields.io/badge/Migrate-4.1.0-green?style=flat-square)

### Frontend Technologies
![Jinja2](https://img.shields.io/badge/Jinja2-3.1.6-red?style=flat-square)
![CSS3](https://img.shields.io/badge/CSS3-Responsive-blue?style=flat-square&logo=css3)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow?style=flat-square&logo=javascript)
![Socket.IO-Client](https://img.shields.io/badge/Socket.IO_Client-Live-black?style=flat-square)

</div>

### 📦 Backend Stack
- **Framework**: Flask 3.1.2 (Python)
- **Database**: SQLite with Flask-SQLAlchemy ORM
- **Real-time**: Flask-SocketIO 5.5.1 for WebSocket communication
- **Authentication**: Flask-Bcrypt 1.0.1 for secure password hashing
- **Migrations**: Flask-Migrate 4.1.0 for database version control
- **CORS**: Flask-CORS 6.0.1 for API endpoint support

### 🎨 Frontend Stack
- **Templates**: Jinja2 3.1.6 templating engine
- **Styling**: CSS3 with responsive design and animations
- **JavaScript**: Vanilla JavaScript with Socket.IO client
- **Real-time UI**: Live notification system and interactive components

### 🔧 Infrastructure
- **Environment**: Python virtual environment (.venv)
- **Configuration**: python-dotenv 1.1.1 for environment variables
- **Database**: SQLite (instance/mealmate.db)

---

## 📁 Project Structure

```
MealMate/
├── 📄 app.py                      # Main Flask application with Socket.IO
├── 📄 models.py                   # Database models and relationships
├── 📄 run.py                      # Application runner with environment support
├── 📄 init_db.py                  # Database initialization with sample data
├── 📄 requirements.txt            # Python dependencies
├── 📄 .env.example                # Environment variables template
├── 📄 .gitignore                  # Git ignore rules
├── 📄 README.md                   # Project documentation (this file)
│
├── 📁 migrations/                 # Database migration files (Flask-Migrate)
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── README
│
├── 📁 instance/                   # Instance-specific files
│   └── mealmate.db               # SQLite database file
│
├── 📁 templates/                  # Jinja2 templates
│   ├── index.html                # Main application page with real-time UI
│   └── admin/                    # Admin panel templates
│       ├── base.html             # Admin base template
│       ├── dashboard.html        # Admin dashboard
│       ├── food_posts.html       # Food posts management
│       ├── hotels.html           # Hotels management
│       ├── login.html            # Admin login page
│       ├── reviews.html          # Reviews management
│       └── users.html            # Users management
│
└── 📁 static/                     # Static assets
    ├── css/
    │   ├── styles.css            # Main styles with notification components
    │   └── admin.css             # Admin panel styles
    ├── js/
    │   ├── script.js             # Frontend JavaScript with real-time features
    │   └── admin.js              # Admin panel JavaScript
    └── uploads/                  # User-uploaded images
```

---

## 🔧 Installation & Setup

<div align="center">

### 📋 Prerequisites

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)
![pip](https://img.shields.io/badge/pip-Latest-green?style=for-the-badge&logo=pypi&logoColor=white)

</div>

### 🚀 Step-by-step Installation

```bash
# 1️⃣ Clone the repository
git clone https://github.com/avishek-sarkar/MealMate.git
cd MealMate

# 2️⃣ Create virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Environment setup
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env

# Edit .env with your configuration

# 5️⃣ Initialize database
python init_db.py

# 6️⃣ Run the application
python run.py
# or
python app.py

# 7️⃣ Access the application
# Open your browser and navigate to http://127.0.0.1:5000
```

<div align="center">

### 🎉 Ready to Go!

Your MealMate application is now running at `http://127.0.0.1:5000`

</div>

---

## 🎯 Default Login Credentials

<div align="center">

### 🔑 Quick Login Reference

<table>
<tr>
<th>👤 User Type</th>
<th>📧 Username Options</th>
<th>🔒 Password</th>
<th>📋 Role Description</th>
</tr>
<tr>
<td align="center"><strong>👨‍💼 Admin</strong></td>
<td><code>admin</code></td>
<td><code>admin123</code></td>
<td>Full system administration access</td>
</tr>
<tr>
<td align="center"><strong>🎓 Students</strong></td>
<td><code>avishek_sarkar</code><br><code>tamim5</code><br><code>mridula</code></td>
<td><code>password123</code></td>
<td>Post reviews & homemade food</td>
</tr>
<tr>
<td align="center"><strong>🏨 Hotel Owners</strong></td>
<td><code>hotel_sareng</code><br><code>mastercafe</code><br><code>chondrobindu</code></td>
<td><code>hotel123</code></td>
<td>Manage restaurant menus</td>
</tr>
</table>

</div>

> **💡 Quick Tip:**
> - **Students**: Any student username + `password123`
> - **Hotel Owners**: Any hotel username + `hotel123`
> - **Admin**: `admin` + `admin123`

> **⚠️ Important Note**: Most users and hotels require admin approval before they can fully use the system.

---

## 🌟 Key Features Detailed

### 🔔 Real-time Notification System
```javascript
✅ Live Notifications       // Instant alerts for likes, comments, and new posts
✅ WebSocket Integration    // Socket.IO for real-time bidirectional communication
✅ User Rooms              // Personalized notification delivery
✅ Notification Bell       // Animated UI component with unread count
✅ Toast Messages          // Non-intrusive popup notifications
```

### 🔐 Authentication & Authorization
```python
✅ Multi-role System       # Students, Hotel Owners, and Admins
✅ Secure Sessions         # Flask session management
✅ Password Hashing        # Bcrypt for secure password storage
✅ Admin Approval          # User approval workflow for security
```

### 📝 Content Management
```yaml
24-hour Expiry: Automatic content cleanup for freshness
Real-time Updates: Live content updates across all users
Image Support: Upload and display food images
Rich Interactions: Like, comment, and share functionality
```

### 🗄️ Database Architecture
- **SQLAlchemy ORM**: Modern database interactions
- **Relationship Management**: Foreign keys and proper relationships
- **Migration Support**: Database versioning with Flask-Migrate
- **Data Integrity**: Proper constraints and validations

---

## 🔒 Security Features

<div align="center">

| 🛡️ Feature | 📝 Description |
|:---|:---|
| **Environment Variables** | Sensitive data protection with `.env` |
| **CSRF Protection** | Cross-site request forgery prevention |
| **Input Validation** | Server-side validation for all inputs |
| **Secure Sessions** | Flask session security with secret keys |
| **Password Security** | Bcrypt hashing with salt |
| **SQL Injection Prevention** | ORM-based database queries |

</div>

---

## 📚 API Documentation

### 🔐 Authentication Endpoints
```http
POST   /login              # User authentication
POST   /logout             # User logout
POST   /register           # Student registration
POST   /register-hotel     # Hotel owner registration
```

### 🔔 Real-time API Endpoints
```http
GET    /api/notifications                    # Get user notifications
POST   /api/post/like                       # Like/unlike posts
POST   /api/post/comment                    # Add comments to posts
GET    /api/post/interactions/<id>/<type>   # Get interaction counts
```

### 📝 Content API Endpoints
```http
GET    /api/posts          # Get all posts
GET    /api/hotels         # Get hotel information
GET    /api/homemade-food  # Get homemade food listings
```

### 🏨 Hotel Owner Endpoints
```http
POST   /add-menu-item                    # Add new menu item
DELETE /delete-menu-item/<item_id>       # Delete menu item
PUT    /toggle-menu-availability/<id>    # Toggle item availability
PUT    /update-menu-item/<item_id>       # Update menu item details
GET    /menu-stats                       # Get menu analytics
GET    /my-menu                          # Get owner's menu items
```

### 👨‍💼 Admin Panel Endpoints
```http
GET    /admin/dashboard              # Admin dashboard
GET    /admin/users                  # User management
GET    /admin/hotels                 # Hotel management
GET    /admin/reviews                # Review management
GET    /admin/food-posts             # Food posts management
POST   /admin/approve-user/<id>      # Approve user
POST   /admin/approve-hotel/<id>     # Approve hotel
DELETE /admin/delete-user/<id>       # Delete user
DELETE /admin/delete-hotel/<id>      # Delete hotel
DELETE /admin/delete-review/<id>     # Delete review
DELETE /admin/delete-food-post/<id>  # Delete food post
```

---

## 🧪 Testing

The application includes comprehensive testing capabilities for:

- ✅ **Database Testing**: Model relationships and data integrity
- ✅ **API Testing**: Endpoint functionality and security
- ✅ **Real-time Testing**: WebSocket communication and notifications
- ✅ **Authentication Testing**: Login/logout and session management

---

## 🚀 Development

### 📝 Code Standards
- **PEP 8**: Python coding standards compliance
- **Documentation**: Comprehensive code documentation
- **Error Handling**: Robust error handling and logging
- **Modular Design**: Separated concerns and clean architecture

### 🔄 Development Workflow
1. 🍴 Fork the repository
2. 🌿 Create a feature branch
3. ✍️ Make your changes with proper testing
4. 📖 Update documentation as needed
5. 🔀 Submit a pull request

---

## 🔮 Future Enhancements

<div align="center">

### 🎯 Planned Features

| Feature | Description | Status |
|:---|:---|:---:|
| 📱 **Mobile App** | React Native mobile application | 🔜 |
| 💳 **Payment Integration** | bKash/Nagad payment gateway | 🔜 |
| 🤖 **AI Recommendations** | AI-powered food recommendations | 🔜 |
| 🚚 **Delivery System** | Campus delivery tracking | 🔜 |
| 📊 **Rating Analytics** | Advanced rating and review analytics | 🔜 |
| 🌐 **Multi-language** | Bengali language support | 🔜 |

### ⚙️ Technical Improvements

| Improvement | Description | Priority |
|:---|:---|:---:|
| 🐘 **PostgreSQL** | Production database migration | 🔴 High |
| 💾 **Redis** | Caching and session storage | 🟡 Medium |
| 🐳 **Docker** | Containerization for deployment | 🔴 High |
| 🔄 **CI/CD** | Automated testing and deployment | 🟡 Medium |
| 📈 **Monitoring** | Application performance monitoring | 🟢 Low |

</div>

---

## 📄 License

<div align="center">

This project is open source and available under the **MIT License**.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

</div>

---

## 🤝 Contributing

<div align="center">

We welcome contributions! ❤️

<p align="center">
  <img src="https://contrib.rocks/image?repo=avishek-sarkar/MealMate" alt="Contributors" />
</p>

**Ways to Contribute:**
- 🐛 Report bugs
- 💡 Suggest new features
- 📖 Improve documentation
- 🔧 Submit pull requests

</div>

---

## 📞 Support

<div align="center">

Need help? We're here for you!

[![GitHub Issues](https://img.shields.io/github/issues/avishek-sarkar/MealMate?style=for-the-badge)](https://github.com/avishek-sarkar/MealMate/issues)
[![GitHub Discussions](https://img.shields.io/github/discussions/avishek-sarkar/MealMate?style=for-the-badge)](https://github.com/avishek-sarkar/MealMate/discussions)

**Get Support:**
- 🐛 [Open an issue](https://github.com/avishek-sarkar/MealMate/issues)
- 💬 [Join discussions](https://github.com/avishek-sarkar/MealMate/discussions)
- 📧 Contact the development team

</div>

---

<div align="center">

## 🎉 MealMate

**Connecting food lovers with real-time experiences, one meal at a time!** 🍽️✨

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=100&section=footer" alt="Footer" />
</p>

*Made with ❤️ for Trishal Campus students by [Avishek Sarkar](https://github.com/avishek-sarkar)*

<p align="center">
  <a href="#-mealmate---trishal-campus-food-hub-">⬆️ Back to Top</a>
</p>

</div>
