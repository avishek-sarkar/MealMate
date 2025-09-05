# MealMate Flask Project Structure

## 📁 Current Project Structure

```
MealMate/
├── 📂 .venv/                    # Python virtual environment
├── 📂 .git/                     # Git repository
├── 📂 static/                   # Static files (CSS, JS, images)
│   ├── 📂 css/
│   │   └── styles.css           # Main stylesheet
│   └── 📂 js/
│       └── script.js            # JavaScript functionality
├── 📂 templates/                # Jinja2 templates
│   └── index.html              # Main template
├── 📄 app.py                   # Main Flask application
├── 📄 run.py                   # Application runner
├── 📄 requirements.txt         # Python dependencies
├── 📄 .env                     # Environment variables
└── 📄 README.md               # Project documentation
```

## 🚀 How to Run

1. **Activate Virtual Environment** (if needed):
   ```bash
   .\.venv\Scripts\activate
   ```

2. **Start the Flask Server**:
   ```bash
   python run.py
   ```

3. **Access the Application**:
   - Open your browser and go to: `http://127.0.0.1:5000`
   - Or click: http://localhost:5000

## ✅ What's Working

### ✅ **Flask Backend Features**
- ✅ **Jinja2 Templates** - Dynamic content rendering
- ✅ **User Authentication** - Login/Register system
- ✅ **Session Management** - User sessions with Flask
- ✅ **API Endpoints** - RESTful API for posts, hotels, food
- ✅ **24-Hour Content Expiry** - Automatic cleanup of old posts
- ✅ **Real-time Updates** - Dynamic content loading

### ✅ **Frontend Features**  
- ✅ **Responsive Design** - Mobile-first approach
- ✅ **Interactive UI** - Like, comment, filter functionality
- ✅ **Authentication Modals** - Login/Register forms
- ✅ **Dynamic Content** - Server-side rendered with Jinja2
- ✅ **AJAX Integration** - API calls for interactions

### ✅ **Backend Architecture**
- ✅ **MVC Pattern** - Routes, templates, static files
- ✅ **Mock Data** - Ready for database integration
- ✅ **Environment Configuration** - .env file setup
- ✅ **Error Handling** - Proper HTTP responses
- ✅ **CORS Support** - Cross-origin requests enabled

## 🔄 Removed Files

The following files were removed as they're no longer needed for Flask:

- ❌ `index.html` (root) → moved to `templates/index.html`
- ❌ `script.js` (root) → moved to `static/js/script.js`  
- ❌ `styles.css` (root) → moved to `static/css/styles.css`
- ❌ `package.json` → not needed for Flask/Python

## 🎯 Next Steps for Production

1. **Database Integration**: Replace mock data with SQLite/PostgreSQL
2. **User Authentication**: Add password hashing and JWT tokens  
3. **File Uploads**: Add image upload functionality
4. **Real-time Features**: WebSocket integration for live updates
5. **Deployment**: Deploy to Heroku, AWS, or DigitalOcean

## 🌐 API Endpoints Available

- `GET /` - Main page with all content
- `POST /login` - User login
- `POST /register` - User registration  
- `GET /logout` - User logout
- `GET /api/posts` - Get posts (with filtering)
- `GET /api/hotels` - Get hotel data
- `GET /api/homemade-food` - Get homemade food (with sorting)
- `POST /api/posts/:id/like` - Like/unlike posts
- `POST /api/posts` - Create new post

Your MealMate Flask application is now ready for development and testing! 🎉
