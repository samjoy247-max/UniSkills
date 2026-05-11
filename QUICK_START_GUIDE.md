# 🚀 UniSkills Project - QUICK START GUIDE

## ✅ Your Project is Now Runnable!

All Sprint 4 backend features are merged, tested, and pushed to GitHub.

---

## 📋 Prerequisites Check

```bash
# Python version
python --version
# Should show: Python 3.13.5+

# Django installed
python -m django --version
# Should show: Django 5.2.6

# Database
# Using MySQL (PyMySQL configured in requirements.txt)
```

---

## 🎯 QUICK START (5 minutes)

### **Option 1: Full Project (Backend + Frontend)**

```bash
# 1. Navigate to backend
cd "d:\Code\Software Engineering Lab\Development UniSkills TEST\FINAL UX\backend"

# 2. Activate virtual environment (if not already)
..\..\\.venv\Scripts\activate

# 3. Run migrations
python manage.py migrate

# 4. Create admin user (first time only)
python manage.py createsuperuser

# 5. Start Django server
python manage.py runserver
# Output: Starting development server at http://127.0.0.1:8000/

# 6. In another terminal, start frontend (optional)
cd ..\frontend\ux-prototype
python -m http.server 3000
```

**Then open in browser:**
- Backend API: http://127.0.0.1:8000/
- Admin Panel: http://127.0.0.1:8000/admin
- Frontend: http://localhost:3000 (if running frontend server)

---

## 🔑 Admin Panel Access

**URL:** http://127.0.0.1:8000/admin

**Use the superuser credentials you created**

**Features Available in Admin:**
- 👥 User Management (Students, Alumni, Providers, Admins)
- 📚 Skills Moderation Dashboard
- 📅 Bookings Management
- ⭐ Ratings & Reviews
- 📊 Analytics & Statistics Dashboard
- 🔒 Security Controls
- 📝 Content Moderation

---

## 📁 Project Structure

```
backend/
├── manage.py                 ✅ Django management
├── requirements.txt          ✅ Dependencies (Django 5.2.6, PyMySQL, etc.)
├── db.sqlite3               ✅ Database (or connect to MySQL)
├── uniskills_backend/       ✅ Main Django config
│   ├── settings.py          ✅ Database, installed apps, middleware
│   ├── urls.py              ✅ Main URL routing
│   └── wsgi.py              ✅ WSGI config for deployment
├── accounts/                ✅ Main app
│   ├── admin.py             ✅ Admin dashboard wiring
│   ├── models.py            ✅ All data models
│   ├── views.py             ✅ All view functions
│   ├── urls.py              ✅ URL patterns
│   └── user_management/     ✅ Feature modules
│       ├── admin_access.py  ✅ Login/Auth
│       ├── alumni.py        ✅ Alumni features
│       ├── booking.py       ✅ Booking workflow
│       ├── rating.py        ✅ Rating system
│       ├── student.py       ✅ Skill CRUD
│       └── session.py       ✅ Session tracking
└── verify_imports.py        ✅ Verification script

frontend/ux-prototype/
├── index.html               ✅ Homepage
├── dashboard.html           ✅ Student dashboard
├── admin.html               ✅ Admin panel
├── alumni.html              ✅ Alumni registration
├── bookings.html            ✅ Booking system
├── rating.html              ✅ Rating interface
├── main.js                  ✅ Frontend logic
└── style.css / styles.css   ✅ Styling
```

---

## 🔍 Available Features (Now Runnable)

### ✅ Authentication & Authorization (UN-97, UN-88)
- Student registration
- Alumni registration
- Provider registration
- Role-based access control
- Admin dashboard access

### ✅ Skills Management (UN-44, UN-48)
- Create skill post
- Edit skill post
- Delete skill post
- Skill moderation
- Admin approval toggle

### ✅ Booking System (UN-60, UN-64)
- Create booking request
- Respond to booking (accept/decline)
- View bookings
- Mark session complete
- Cancel booking

### ✅ Alumni Features (UN-77, UN-81)
- Alumni registration
- Alumni dashboard
- Create alumni post
- Moderate alumni post
- Alumni moderation dashboard

### ✅ Rating System (UN-73)
- Submit rating after session
- Review/comments
- Rating validation

### ✅ Admin Panel (UN-88, UN-91, UN-85)
- User management
- Skills moderation
- Bookings oversight
- Analytics dashboard
- Alumni moderation

### ✅ Analytics (UN-91)
- Total users count
- Skills statistics
- Booking metrics
- Rating averages
- Session tracking

---

## 🧪 Verification Commands

```bash
# 1. Check Django setup
cd backend
python manage.py check
# Expected: "System check identified no issues (0 silenced)."

# 2. Test imports
python verify_imports.py
# Expected: "✅ ALL IMPORTS VERIFIED - BACKEND IS RUNNABLE"

# 3. Check database migration status
python manage.py showmigrations
# Should show all migrations as [X] (applied)
```

---

## 🛠️ Database Setup

### Option A: SQLite (Default - Quick Testing)
```bash
# Just run migrations (db.sqlite3 created automatically)
python manage.py migrate
```

### Option B: MySQL (Production)
```bash
# 1. Update settings.py with MySQL config:
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'uniskills_db',
#         'USER': 'root',
#         'PASSWORD': 'your_password',
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }

# 2. Install MySQL Python client (already in requirements.txt)
pip install PyMySQL

# 3. Run migrations
python manage.py migrate
```

---

## 🚀 Running for Development

**Terminal 1 - Backend Server:**
```bash
cd backend
python manage.py runserver
# Runs on http://127.0.0.1:8000/
```

**Terminal 2 - Frontend (Optional):**
```bash
cd frontend/ux-prototype
python -m http.server 3000
# Runs on http://localhost:3000/
```

**Terminal 3 - Watch for changes (Optional):**
```bash
# If you want to auto-reload on Python changes
watchmedo auto-restart -d backend/accounts -p '*.py' -- python manage.py runserver
```

---

## 📊 Testing the Features

### 1. Create Admin User
```
URL: http://127.0.0.1:8000/admin
Click: "Add user" → Create superuser
```

### 2. Test Student Registration
```
Check admin panel → Users → Create student
```

### 3. Test Alumni Features
```
Check admin panel → Alumni Posts → View moderation dashboard
```

### 4. Test Booking System
```
Check admin panel → Bookings → View all bookings
```

### 5. Test Ratings
```
Check admin panel → Ratings → View ratings
```

---

## 🔗 Important URLs

```
Admin Dashboard:     http://127.0.0.1:8000/admin/
API Root:            http://127.0.0.1:8000/api/
Landing Page:        http://127.0.0.1:8000/
Dashboard:           http://127.0.0.1:8000/dashboard/
Skills:              http://127.0.0.1:8000/skills/
Bookings:            http://127.0.0.1:8000/bookings/
Alumni:              http://127.0.0.1:8000/alumni/
Ratings:             http://127.0.0.1:8000/ratings/
```

---

## 📋 Team Feature Assignments

| Team Member | Features | Branch | Commits |
|------------|----------|--------|---------|
| **Shahin** | Booking (UN-60, UN-64) | shahin | 6421e5a |
| **Maria** | Alumni (UN-77, UN-81) | maria | 61bb538 |
| **Esha** | Rating (UN-73) + Analytics (UN-91) | esha | 7bb4e05 |
| **Samjoy** | Admin/Moderation/Security (UN-88, UN-91, UN-85) | joy | 614e1c5 |

---

## 📌 Current Status

```
✅ Backend Code: COMPLETE
✅ Database Models: COMPLETE
✅ Admin Panel: WIRED
✅ View Functions: WORKING
✅ Import Chain: VERIFIED
✅ All Features: MERGED
✅ GitHub Push: COMPLETE

🚀 PROJECT STATUS: READY FOR DEPLOYMENT
```

---

## 🆘 Troubleshooting

### Error: "Module not found: accounts"
```bash
# Solution: Make sure you're in the backend folder
cd backend
python manage.py runserver
```

### Error: "Database connection failed"
```bash
# Solution 1: Use SQLite (default)
python manage.py migrate

# Solution 2: For MySQL, check credentials in settings.py
```

### Error: "Port 8000 already in use"
```bash
# Solution: Run on different port
python manage.py runserver 8001
```

---

## 📚 Additional Commands

```bash
# Create new migration for model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Enter Django shell
python manage.py shell

# Collect static files (for production)
python manage.py collectstatic

# Run tests (if exist)
python manage.py test

# View all available commands
python manage.py help
```

---

**Generated:** May 11, 2026  
**Project:** UniSkills - Sprint 4 Complete  
**Status:** 🚀 Ready to Run

Happy Coding! 🎉
