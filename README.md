# MealMate - Professional Food Community Platform

A modern Flask-based web application for food enthusiasts to share reviews, discover restaurants, and connect with homemade food sellers.

## 🚀 Features

- **Food Reviews & Posts**: Share experiences with restaurants and dishes
- **Hotel Discovery**: Browse and discover local restaurants
- **Homemade Food Marketplace**: Connect with local home cooks
- **User Authentication**: Secure login and registration system
- **Real-time Content**: 24-hour content expiry system
- **Responsive Design**: Mobile-friendly interface
- **Professional UI**: Clean, modern design with smooth animations

## �️ Technology Stack

- **Backend**: Flask 2.3.3 (Python)
- **Frontend**: Jinja2 templates with vanilla JavaScript
- **Styling**: CSS3 with responsive design
- **Dependencies**: Listed in `requirements.txt`

## 📁 Project Structure

```
MealMate/
├── app.py              # Main Flask application
├── run.py              # Application runner
├── requirements.txt    # Python dependencies
├── .env.example       # Environment variables template
├── .gitignore         # Git ignore rules
├── README.md          # Project documentation
├── templates/         # Jinja2 templates
│   └── index.html     # Main application template
└── static/           # Static assets
    ├── css/
    │   └── styles.css # Application styles
    └── js/
        └── script.js  # Frontend JavaScript
```

## 🔧 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd MealMate
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment setup**
   ```bash
   copy .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the application**
   ```bash
   python run.py
   # or
   python app.py
   ```

6. **Access the application**
   Open your browser and navigate to `http://127.0.0.1:5000`

## 🌟 Key Features

### Authentication System
- Secure user registration and login
- Session management with Flask sessions
- Form-based authentication

### Content Management
- 24-hour content expiry system
- Real-time time remaining indicators
- Dynamic content filtering

### API Endpoints
- RESTful API for posts, hotels, and homemade food
- JSON responses for frontend integration
- Error handling and validation

### Responsive Design
- Mobile-first responsive layout
- Smooth animations and transitions
- Professional UI/UX design

## 🔒 Security Features

- Environment variable management
- Gitignore protection for sensitive files
- Input validation and sanitization
- Secure session handling

## 🚀 Development

### Code Organization
- Professional code structure with proper documentation
- Separated concerns (routes, utilities, data models)
- Clean, maintainable codebase

### Standards
- PEP 8 Python coding standards
- Consistent naming conventions
- Comprehensive error handling
- Professional documentation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## � License

This project is open source and available under the [MIT License](LICENSE).

## 🔮 Future Enhancements

- Database integration (PostgreSQL/MongoDB)
- Real-time messaging system
- Advanced search and filtering
- Payment integration for marketplace
- Mobile app development
- API rate limiting and authentication
- Admin dashboard
- Analytics and reporting

## � Support

For questions or support, please open an issue on the repository.

---

**MealMate** - Connecting food lovers, one meal at a time! 🍽️
