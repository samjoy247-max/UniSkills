# UniSkills Platform - Complete Setup Guide

## 📦 Quick Start (After Clone)

### **Windows:**
```bash
git clone <your-repo-url>
cd FINAL\ UX
copy .env.example .env
# Edit .env with your MySQL credentials
setup_database.bat
python backend/manage.py runserver
```

### **Linux/Mac:**
```bash
git clone <your-repo-url>
cd FINAL\ UX
cp .env.example .env
# Edit .env with your MySQL credentials
chmod +x setup_database.sh
./setup_database.sh
python backend/manage.py runserver
```

---

## 📋 Prerequisites

1. **Python 3.9+**
   ```bash
   python --version
   ```

2. **MySQL Server 5.7+**
   ```bash
   mysql --version
   # Ensure MySQL is running
   # Windows: Services > MySQL80
   # Linux: sudo systemctl start mysql
   # Mac: brew services start mysql
   ```

3. **Virtual Environment (Recommended)**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   ```

4. **Install Dependencies**
   ```bash
   pip install -r backend/requirements.txt
   ```

---

## 🗄️ Database Configuration

### Create `.env` file from template:
```bash
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
```

### Edit `.env` with your MySQL credentials:
```ini
MYSQL_DATABASE=uniskills_test
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
```

### Run database setup (Windows):
```bash
setup_database.bat
```

Or manually:
```bash
cd backend
python manage.py migrate
python manage.py shell < ../init_database.py
cd ..
```

---

## 👥 Test User Credentials

After setup, test with these users:

| Role | Username | Password | Email |
|------|----------|----------|-------|
| Admin | admin | admin | admin@uniskills.edu |
| Student | student1 | student123 | student1@uap-bd.edu |
| Instructor | instructor1 | instructor123 | instructor1@uap-bd.edu |
| Alumni | alumni1 | alumni123 | alumni1@uap-bd.edu |

---

## 🚀 Running the Server

```bash
cd backend
python manage.py runserver
```

Visit: **http://localhost:8000**

---

## 📁 Project Structure

```
FINAL UX/
├── backend/
│   ├── accounts/
│   │   ├── models.py           # All 10 models (User, Skill, Booking, etc)
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── user_management/    # Function-based views
│   │   │   ├── student.py
│   │   │   ├── alumni.py
│   │   │   ├── admin_access.py
│   │   │   └── __init__.py
│   │   ├── otp_utils.py        # OTP generation & email
│   │   ├── migrations/
│   │   └── admin.py
│   ├── uniskills_backend/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── templates/              # Django templates
│   ├── static/                 # CSS, JS, images
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   └── ux-prototype/           # Original UI designs (HTML/CSS/JS)
├── docs/
│   ├── DEVELOPMENT_WORKFLOW.md # Team assignments & Git workflow
│   └── FINAL_API_DOCUMENTATION.docx
├── .env.example                # Database config template
├── setup_database.bat          # Windows database setup
├── setup_database.sh           # Linux/Mac database setup
└── init_database.py            # Create test data

```

---

## 🔄 Git Workflow for Team

### Before starting a task:
```bash
git pull origin develop
git checkout -b feature/UN-XX-taskname
```

### After implementing:
```bash
git add <modified_files>
git commit -m "UN-XX: Brief description - YourName"
git push origin feature/UN-XX-taskname
```

### After all team reviews:
```bash
git checkout develop
git pull origin develop
git merge feature/UN-XX-taskname
git push origin develop
```

---

## 📋 Implementation Checklist

When implementing a feature, ensure:

- [ ] All models defined in `accounts/models.py`
- [ ] Form validations in `accounts/forms.py`
- [ ] Views in `accounts/user_management/<role>.py`
- [ ] URL routes in `accounts/urls.py`
- [ ] Templates in `templates/`
- [ ] CSRF tokens on all POST forms
- [ ] @login_required on protected views
- [ ] @staff_member_required on admin views
- [ ] Database migrations run without errors
- [ ] Test data loads correctly
- [ ] No duplicate function definitions

---

## 🧪 Testing Features

### Run Django development server:
```bash
python backend/manage.py runserver
```

### Access admin panel:
```
http://localhost:8000/admin/
Username: admin
Password: admin
```

### Test each feature:
1. **Registration**: /register/student/, /register/alumni/
2. **Login**: /login/
3. **Dashboard**: /dashboard/ (after login)
4. **Skills**: /skills.html (browse), create skill (if instructor)
5. **Moderation**: /moderation.html (if admin)
6. **Bookings**: /bookings.html
7. **Ratings**: /rating.html

---

## 🐛 Troubleshooting

### "MySQL connection refused"
- Ensure MySQL is running
- Check credentials in .env file
- Verify MySQL port (default 3306)

### "ModuleNotFoundError"
- Activate virtual environment
- Run: `pip install -r backend/requirements.txt`

### "Database doesn't exist"
- Run: `setup_database.bat` or `./setup_database.sh`

### "Migrations pending"
- Run: `python backend/manage.py migrate`

### "OTP email not sending"
- Configure email in .env file
- Check spam folder
- Test with Django shell: `python backend/manage.py shell`

---

## 📚 Feature Documentation

For detailed API documentation, see:
- `FINAL_API_DOCUMENTATION.docx` - Complete endpoint reference
- `FINAL_API_VIVA.html` - Interactive endpoint guide
- `DEVELOPMENT_WORKFLOW.md` - Team workflow & assignments

---

## 🎯 Current Development Phase

**Phase 1: Skill Management System**
- UN-44: Create Skill Posts (Assigned to Joy) 
- UN-48: Moderation (Assigned to Shahin)
- UN-52: Search & Filter (Assigned to Esha)
- UN-56: Browse Skills (Assigned to Maria)

See `DEVELOPMENT_WORKFLOW.md` for detailed assignments and file lists.

---

## 📞 Contact & Support

For questions or issues, refer to:
1. `DEVELOPMENT_WORKFLOW.md` - Task assignments
2. `FINAL_API_VIVA.html` - API reference
3. Django documentation - Framework questions
4. Team members - Assigned to each task

---

**Last Updated:** May 9, 2026  
**Version:** 1.0  
**Status:** Development Phase 1
