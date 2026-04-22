<div align="center">

# MealMate

<p align="center">
  <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=26&duration=2800&pause=1000&color=FF6B35&center=true&vCenter=true&width=620&lines=Connecting+Food+Lovers;Real-time+Campus+Food+Reviews;Discover+Posts%2C+Hotels%2C+and+Homemade+Food" alt="Typing SVG" />
</p>

[![Flask](https://img.shields.io/badge/Flask-3.1.2-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Socket.IO](https://img.shields.io/badge/Socket.IO-5.5.1-010101?style=flat-square&logo=socket.io&logoColor=white)](https://socket.io/)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

<p align="center">
  A Flask web application for food reviews, hotel discovery, homemade food posts, and real-time notifications.
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#technology-stack">Technology</a> •
  <a href="#project-structure">Structure</a> •
  <a href="#installation--setup">Setup</a> •
  <a href="#default-login-credentials">Login</a> •
  <a href="#api-documentation">API</a>
</p>

</div>

---

## Overview

MealMate is built for a campus food community where students can share reviews, explore restaurants, post homemade food, and get live updates through Socket.IO notifications. The project combines a clean Flask backend, a responsive front end, and an admin workflow for content moderation.

### Quick Facts

| Item | Details |
|:---|:---|
| Framework | Flask 3.1.2 |
| Database | SQLite with Flask-SQLAlchemy |
| Real-time Layer | Flask-SocketIO 5.5.1 |
| Authentication | Werkzeug password hashing |
| Migrations | Flask-Migrate |
| License | MIT |

---

## Features

### Core Product Areas
- **Food reviews and posts**: Share experiences with local restaurants and dishes.
- **Hotel discovery**: Browse restaurants and view menu-related information.
- **Homemade food marketplace**: Post homemade food items for nearby users.
- **Hotel owner dashboard**: Manage menu items and track listing activity.
- **User authentication**: Separate flows for students, hotel owners, and admins.
- **Admin panel**: Manage users, hotels, reviews, and food posts from one place.

### Real-time Experience
- **Live notifications**: New posts, likes, and comments appear instantly.
- **Real-time interactions**: Post activity updates without page reloads.
- **Socket.IO integration**: WebSocket communication between clients and server.
- **Notification bell**: Unread count and animated notification state.
- **Broadcast updates**: New content can be shown to all connected users.
- **Live comments**: Comment submission with immediate feedback.

### Platform Enhancements
- **Content expiry**: Older content can be cleaned automatically.
- **Responsive layout**: Works across desktop and mobile screens.
- **Database integration**: SQLAlchemy models with relational structure.
- **API endpoints**: JSON endpoints for content, interactions, and notifications.
- **Local context**: Pricing and content conventions align with campus life.

---

## Technology Stack

### Frontend
- **Jinja2 3.1.6** templates.
- **CSS** with responsive layout and animation support.
- **Vanilla JavaScript** with a Socket.IO client.
- **Admin UI** for moderation and management tasks.

### Backend
- **Flask 3.1.2** for the web application.
- **SQLite** with **Flask-SQLAlchemy 3.1.1** for persistence.
- **Flask-SocketIO 5.5.1** for live notification delivery.
- **Werkzeug security** helpers for password hashing and verification.
- **Flask-Migrate 4.1.0** and **Alembic** for schema versioning.

### Environment
- **Python virtual environment** in `.venv`.
- **python-dotenv 1.1.1** for environment variables.
- **SQLite database** stored in `instance/mealmate.db`.

---

## Project Structure

```text
MealMate/
├── app.py
├── init_db.py
├── LICENSE
├── models.py
├── README.md
├── requirements.txt
├── run.py
├── .env.example
├── .gitignore
├── instance/
│   └── mealmate.db
├── migrations/
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── README
├── static/
│   ├── css/
│   │   ├── styles.css
│   │   └── admin.css
│   ├── js/
│   │   ├── script.js
│   │   └── admin.js
│   └── uploads/
└── templates/
    ├── index.html
    └── admin/
        ├── base.html
        ├── dashboard.html
        ├── food_posts.html
        ├── hotels.html
        ├── login.html
        ├── reviews.html
        └── users.html
```

---

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip

### Setup Steps
1. Clone the repository.
   ```bash
   git clone https://github.com/avishek-sarkar/MealMate.git
   cd MealMate
   ```
2. Create and activate a virtual environment.
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
   On Linux or macOS, use `source .venv/bin/activate`.
3. Install dependencies.
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment variables.
   ```bash
   copy .env.example .env
   ```
   Then update `.env` with your local values.
5. Initialize the database.
   ```bash
   python init_db.py
   ```
6. Start the application.
   ```bash
   python run.py
   ```
   You can also run `python app.py` if preferred.
7. Open the app in your browser.
   ```text
   http://127.0.0.1:5000
   ```

---

## Default Login Credentials

| User Type | Username Options | Password | Role |
|:---|:---|:---|:---|
| Admin | `admin` | `admin123` | Full system administration |
| Students | `avishek_sarkar`, `tamim5`, `mridula` | `password123` | Post reviews and homemade food |
| Hotel Owners | `hotel_sareng`, `mastercafe`, `chondrobindu` | `hotel123` | Manage restaurant menus |

**Quick access:**
- Students use any student username with `password123`.
- Hotel owners use any hotel username with `hotel123`.
- Admin uses `admin` with `admin123`.

Most accounts require admin approval before full access is granted.

---

## Key Capabilities

### Real-time Notifications
- Live alerts for posts, likes, and comments.
- Personalized notification delivery through Socket.IO rooms.
- Toast-style feedback for non-intrusive updates.

### Authentication and Authorization
- Multi-role login support for students, hotel owners, and admins.
- Session-based auth with Werkzeug password hashing.
- Admin approval flow for controlled onboarding.

### Content Management
- Image upload support for posts and food listings.
- Live content updates across connected users.
- Automatic cleanup support for older content.

### Database Design
- SQLAlchemy ORM for structured data access.
- Foreign keys and relationships for user, post, and hotel data.
- Flask-Migrate support for schema evolution.

---

## Security Features

| Feature | Description |
|:---|:---|
| Environment variables | Sensitive values stay out of source code. |
| Input validation | Validates data before persistence. |
| Secure sessions | Uses Flask session handling. |
| Role-based access checks | Route guards for user, owner, and admin sessions. |
| Password hashing | Stores passwords with Werkzeug hash utilities. |
| ORM queries | Reduces SQL injection risk. |

---

## API Documentation

### Authentication
```http
POST /login
POST /logout
POST /register
POST /register-hotel
GET  /admin/login
POST /admin/login
GET  /admin/logout
POST /admin/logout
```

### Content and Interactions
```http
GET  /api/posts
GET  /api/hotels
GET  /api/homemade-food
GET  /api/menu-items/<hotel_id>
GET  /api/notifications
POST /api/post/like
POST /api/post/comment
GET  /api/post/interactions/<post_id>/<post_type>
POST /post-review
POST /post-food
POST /cleanup-expired
```

### Hotel Owner Actions
```http
POST   /add-menu-item
DELETE /delete-menu-item/<item_id>
PUT    /toggle-menu-availability/<item_id>
PUT    /update-menu-item/<item_id>
GET    /menu-stats
GET    /my-menu
GET    /my-posts
PUT    /update-profile
POST   /update-profile
PUT    /update-business
POST   /update-business
PUT    /change-password
POST   /change-password
```

### Admin Actions
```http
GET    /admin/dashboard
GET    /admin/users
GET    /admin/hotels
GET    /admin/reviews
GET    /admin/food-posts
POST   /admin/approve-user/<id>
POST   /admin/approve-hotel/<id>
DELETE /admin/delete-user/<id>
DELETE /admin/delete-hotel/<id>
DELETE /admin/delete-review/<id>
DELETE /admin/delete-food-post/<id>
```

---

## Future Enhancements

| Planned Feature | Description | Status |
|:---|:---|:---:|
| Mobile app | React Native companion app | Planned |
| Payment integration | bKash/Nagad support | Planned |
| AI recommendations | Personalized food suggestions | Planned |
| Delivery tracking | Campus delivery flow | Planned |
| Rating analytics | Review insights and trends | Planned |
| Multi-language | Bengali language support | Planned |

| Technical Improvement | Description | Priority |
|:---|:---|:---:|
| PostgreSQL | Production database migration | High |
| Redis | Caching and session storage | Medium |
| Docker | Containerization | High |
| CI/CD | Automated build and deploy | Medium |
| Monitoring | Application performance tracking | Low |

---

## License

MealMate is available under the [MIT License](LICENSE).

---

## Contributing

Contributions are welcome. Please report bugs, suggest improvements, or open pull requests with focused changes.

### Contributors

<p align="center">
   <a href="https://github.com/avishek-sarkar/MealMate/graphs/contributors">
      <img src="https://contrib.rocks/image?repo=avishek-sarkar/MealMate" alt="Contributors" />
   </a>
</p>

---

## Support

- Open an issue on GitHub.
- Start a discussion if you have a question or feature request.
- Contact the maintainers for project-specific support.

---

<div align="center">

**MealMate** - Connecting food lovers with real-time experiences, one meal at a time.

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=90&section=footer" alt="Footer" />
</p>

</div>
