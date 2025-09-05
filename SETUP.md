# MealMate Setup Instructions

## 🚀 Quick Setup Guide

### Prerequisites
- Python 3.8+ installed
- Git installed

### 1. Clone the Repository
```bash
git clone https://github.com/avishek-sarkar/MealMate.git
cd MealMate
git checkout frontend
```

### 2. Set Up Python Virtual Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.\.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
```bash
# Copy environment template
copy .env.example .env

# Edit .env file and update:
# - SECRET_KEY (generate a random string)
# - Other settings as needed
```

### 5. Run the Application
```bash
python run.py
```

### 6. Access the Application
Open your browser and go to: **http://127.0.0.1:5000**

## 🔧 Development Commands

### Start Development Server
```bash
python run.py
```

### Install New Dependencies
```bash
pip install package_name
pip freeze > requirements.txt
```

### Database Commands (Future)
```bash
# Initialize database
flask db init

# Create migration
flask db migrate -m "description"

# Apply migration
flask db upgrade
```

## 📁 Project Structure
```
MealMate/
├── templates/          # Jinja2 HTML templates
├── static/
│   ├── css/           # Stylesheets
│   └── js/            # JavaScript files
├── app.py             # Main Flask application
├── run.py             # Application runner
├── requirements.txt   # Dependencies
├── .env.example       # Environment template
└── .gitignore         # Git ignore rules
```

## 🔒 Security Notes

- Never commit `.env` file to git
- Change `SECRET_KEY` in production
- Use environment variables for sensitive data
- Enable HTTPS in production

## 🚀 Deployment

### Heroku
```bash
# Install Heroku CLI
# Create Procfile
echo "web: python run.py" > Procfile

# Deploy
heroku create your-app-name
git push heroku frontend:main
```

### Local Production
```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🛠️ Troubleshooting

### Common Issues

1. **Import Errors**: Make sure virtual environment is activated
2. **Permission Errors**: Run terminal as administrator (Windows)
3. **Port Already in Use**: Change port in `.env` file
4. **Template Not Found**: Check templates/ directory structure

### Reset Environment
```bash
# Remove virtual environment
rmdir /s .venv

# Recreate from scratch
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## 📧 Support

For issues or questions, create an issue on GitHub or contact the development team.

Happy coding! 🍔💻
