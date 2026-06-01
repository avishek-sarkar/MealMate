<div align="center">

# MealMate

![Typing](https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=24&duration=2800&pause=1000&color=FF6B35&center=true&vCenter=true&width=760&height=56&lines=Connecting+Food+Lovers;Real-time+Campus+Food+Reviews;Discover+Posts%2C+Hotels%2C+and+Homemade+Food)

[![Flask](https://img.shields.io/badge/Flask-3.1.2-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Socket.IO](https://img.shields.io/badge/Socket.IO-5.5.1-010101?style=flat-square&logo=socket.io&logoColor=white)](https://socket.io/)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

</div>

## Project Overview

MealMate is a real-time food discovery and community platform built for campus ecosystems. It connects students, local restaurants, and student cooks in one place, with live updates and a moderated workflow.

## Why It Matters

- Students can find reliable, affordable meals quickly.
- Student cooks get a practical marketplace to sell homemade food.
- Live reviews and notifications improve trust and decision-making.
- Admin moderation and approvals keep the ecosystem safe.

## Technology Stack

- Backend: Python 3.8+, Flask, SQLAlchemy, Werkzeug, Flask-Migrate
- Real-time: Flask-SocketIO, python-socketio
- Frontend: Jinja2 templates, vanilla JavaScript, CSS
- Database: SQLite (development)
- Configuration: python-dotenv

## System Architecture

```mermaid
graph TD
    User[Web User] <--> Web[Flask App]
    Admin[Admin User] <--> Web
    Web --> Auth[Auth and Sessions]
    Web --> Realtime[Socket.IO Events]
    Web --> ORM[SQLAlchemy ORM]
    ORM <--> DB[(SQLite Database)]
    Migrate[Flask-Migrate] --> DB
```

## Database Schema

```mermaid
erDiagram
    ADMIN ||--o{ USER : approves
    ADMIN ||--o{ HOTEL_OWNER : approves
    USER ||--o{ REVIEW : writes
    USER ||--o{ STUDENT_FOOD_POST : creates
    USER ||--o{ NOTIFICATION : receives
    USER ||--o{ POST_INTERACTION : performs
    HOTEL_OWNER ||--o{ MENU_ITEM : manages
    MENU_ITEM ||--o{ REVIEW : receives

    USER {
        int id
        string username
        string email
        string password_hash
    }
    HOTEL_OWNER {
        int id
        string hotel_name
        string email
        string license_number
    }
    MENU_ITEM {
        int id
        string item_name
        float price
        boolean is_available
    }
    STUDENT_FOOD_POST {
        int id
        string title
        float price
        datetime expires_at
    }
```

## Key Capabilities

### All-in-One Platform for Foods

- Students can find and compare foods quickly.
- Hotel-owners can update their menus daily. 
- Selling homemade food becomes easy.
- Review system ensures quality. 

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

### Demo

| Main Homepage | Homemade Food Marketplace |
| --- | --- |
| ![Homepage](Documentation/Homepage.png) | ![Homemade Food](Documentation/Homemade_food.png) |
| **Hotel Menu Discovery** | **Admin Control Panel** |
| ![Hotel Menu](Documentation/Hotel_menu.png) | ![Admin Dashboard](Documentation/Admin_dashboard.png) |

## Security Features

| Feature | Description |
| --- | --- |
| Environment variables | Sensitive values stay out of source code. |
| Input validation | Validates data before persistence. |
| Secure sessions | Uses Flask session handling. |
| Role-based access checks | Route guards for user, owner, and admin sessions. |
| Password hashing | Stores passwords with Werkzeug hash utilities. |
| ORM queries | Reduces SQL injection risk. |

## Installation and Setup

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
3. Install dependencies.
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment variables.
   ```bash
   copy .env.example .env
   ```
5. Initialize the database.
   ```bash
   python init_db.py
   ```
6. Run the server.
   ```bash
   python run.py
   ```
   Open http://127.0.0.1:5000

## Default Credentials

| User Type | Username Options | Password | Notes |
| --- | --- | --- | --- |
| Admin | admin | admin123 | Full access |
| Students | avishek_sarkar, tamim5, mridula | password123 | Admin approval required |
| Hotel Owners | hotel_sareng, mastercafe, chondrobindu | hotel123 | Admin approval required |

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

## API Documentation

See [API_Documentation.md](Documentation/API_Documentation.md) for the complete API reference.

## Future Enhancements

- Mobile app for students and hotel owners.
- Payment integration for direct transactions.
- Recommendations and smarter discovery.
- Delivery workflow and order tracking.
- Production stack upgrades (PostgreSQL, Docker, CI/CD, caching, monitoring).

## Contributing

Contributions are welcome. Please report bugs, suggest improvements, or open pull requests with focused changes.

### Contributors

<p align="center">
   <a href="https://github.com/avishek-sarkar/MealMate/graphs/contributors">
      <img src="https://contrib.rocks/image?repo=avishek-sarkar/MealMate" alt="Contributors" />
   </a>
</p>

---

## Outro

MealMate brings campus food communities together with real-time updates, trustworthy reviews, and structured moderation. Thanks for taking some time to visit this repository. 
