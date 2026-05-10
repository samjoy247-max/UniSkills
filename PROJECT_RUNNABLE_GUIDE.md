# UniSkills Full Project Setup & Demo Guide

**Date:** May 10, 2026  
**Sprint Status:** ✅ COMPLETE  
**All Features:** Backend + Frontend Templates Ready

---

## 🚀 Quick Start (For Demo)

### 1. Activate Virtual Environment (Windows PowerShell)

```powershell
& "D:\Code\Software Engineering Lab\Development UniSkills TEST\.venv\Scripts\Activate.ps1"
cd "FINAL UX\backend"
```

### 2. Install/Verify Dependencies

```bash
pip install -r requirements.txt
```

**Key packages already included:**
- Django 5.2.6
- PyMySQL (for MySQL database)
- Pillow (for image handling)
- djangorestframework (if applicable)

### 3. Apply Database Migrations

```bash
python manage.py migrate
```

This will:
- Create all required tables
- Apply UN-60 (Booking), UN-64 (SessionHistory), UN-85 (AlumniPost), UN-69/UN-73 (Rating) schemas

### 4. Create Superuser (Optional, for Admin Panel)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account for testing moderation features.

### 5. Run Development Server

```bash
python manage.py runserver 0.0.0.0:8000
```

Access the application at: **http://localhost:8000**

### 6. Run Backend Test Suite

```bash
python test_shahin_esha.py
```

**Test Output Includes:**
- UN-64: Session History Tracking ✅
- UN-85: Alumni Post Moderation ✅
- UN-69/UN-73: Rating System ✅

---

## 📋 Features Implemented (Sprint Complete)

### **UN-60: Booking Flow (Joy - samjoy247-max)**
- ✅ Create booking requests
- ✅ Accept/Decline bookings
- ✅ Cancel bookings
- ✅ Mark bookings complete
- ✅ OTP verification at registration (timezone-aware)
- **Files:** `booking.py`, `booking_accept.html`, `booking_decline.html`

### **UN-64: Session History (Shahin - Shahin-100)**
- ✅ Track completed sessions per student/instructor
- ✅ Role-based filtering (student vs instructor view)
- ✅ Session attendance tracking
- **Files:** `session.py`, `session_history.html`, `session_detail.html`, `session_list.html`

### **UN-85: Alumni Post Moderation (Shahin - Shahin-100)**
- ✅ Alumni post creation
- ✅ Approve/reject posts
- ✅ Moderation dashboard
- **Files:** `alumni.py`, `alumni_moderation_dashboard.html`, `alumni_detail.html`, `alumni_list.html`

### **UN-69/UN-73: Rating System (Ayat087/Esha - khadijaesha8@gmail.com)**
- ✅ Post-session rating submission (1-5 stars)
- ✅ Optional feedback text
- ✅ Unique rating per student/skill
- ✅ Automatic average rating calculation
- ✅ Rating dashboard & aggregation
- **Files:** `rating.py`, `rating_form.html`, `rating_detail.html`, `rating_list.html`, `rating_dashboard.html`, `skill_rating_summary.html`

---

## 🗄️ Database Schema

**Key Models Created:**
- `SessionHistory` — tracks completed sessions
- `AlumniPost` — alumni blog/career posts
- `Rating` — post-session student feedback
- `TimeBasedOTP` — OTP for registration (10-min expiry)
- `Booking` — skill booking requests with status tracking
- `CustomUser` — extended user model with role, department, alumni_verified fields

**Migrations Applied:**
- 0004: Initial schema (TimeBasedOTP, AlumniPost, Booking, SessionHistory, Rating)
- 0005: Profile enhancements (profile_picture, is_email_verified)

---

## 📁 Project Structure

```
FINAL UX/
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── test_shahin_esha.py          ← Run this to test all features
│   ├── accounts/
│   │   ├── models.py               ← All models defined
│   │   ├── views.py                ← API endpoints
│   │   ├── urls.py                 ← Routes for all features
│   │   ├── user_management/
│   │   │   ├── booking.py          ← UN-60
│   │   │   ├── session.py          ← UN-64
│   │   │   ├── alumni.py           ← UN-85
│   │   │   ├── rating.py           ← UN-69/UN-73
│   │   │   └── otp_utils.py        ← OTP generation/verification
│   │   ├── migrations/
│   │   │   ├── 0004_initial_schema.py
│   │   │   └── 0005_profile_enhancements.py
│   │   └── templates/accounts/
│   │       ├── booking_*.html      ← Booking templates (Joy)
│   │       ├── alumni_*.html       ← Alumni templates (Shahin)
│   │       ├── session_*.html      ← Session templates (Shahin)
│   │       ├── rating_*.html       ← Rating templates (Ayat087)
│   │       └── verify_otp.html     ← OTP verification (Maria)
│   └── uniskills_backend/
│       └── settings.py
└── frontend/
    └── ux-prototype/               ← Old UX (reference only)
```

---

## 🧪 Testing Strategy

### Backend Tests (Automated)

```bash
python test_shahin_esha.py
```

Tests cover:
- User creation (provider, student, alumni roles)
- Booking CRUD operations
- Session history creation & retrieval
- Alumni post moderation (create, approve, reject)
- Rating submission & average calculation

**All 4 Test Groups Pass:** ✅

---

## 👥 Team Contributions (Balanced)

| Team Member | Jira Stories | Commits | Code Lines | Branch |
|---|---|---|---|---|
| **Joy** (samjoy247-max) | UN-60 | 29 | 8,494 | `joy` |
| **Shahin** (Shahin-100) | UN-64, UN-85 | 7 | 775+ | `shahin` |
| **Ayat087** (Esha981 new) | UN-69, UN-73 | 5 | 432+ | `esha` |
| **Maria** (tanjidaMaria) | HTML Support | 4 | 2,972 | `maria` |

All branches merged into `main` for demo.

---

## 🔐 Default Test Accounts

After running migrations, the test file auto-creates:
- **Provider:** `test_provider_sh_v2`
- **Student:** `test_student_sh_v2`
- **Alumni:** `test_alumni_esha_v2`

(Passwords are set in `test_shahin_esha.py`)

---

## 🛠️ Troubleshooting

### Issue: Database Connection Error
**Solution:** Ensure MySQL is running and `.env` credentials are correct.

### Issue: Migration Fails
**Solution:**
```bash
python manage.py makemigrations accounts
python manage.py migrate
```

### Issue: Missing Template
**Solution:** All templates are in `backend/templates/accounts/`. Ensure Django `TEMPLATES` setting points correctly in `settings.py`.

### Issue: OTP Not Sending
**Solution:** OTP falls back to console output if SMTP not configured. Check Django logs for OTP code.

---

## 📊 Jira Tickets (Ready to Mark Done)

- ✅ **UN-60:** Booking Request Flow
- ✅ **UN-64:** Session History Tracking
- ✅ **UN-85:** Alumni Post Moderation
- ✅ **UN-69:** Rating Submission
- ✅ **UN-73:** Rating Display & Aggregation

All stories have:
- Backend implementation ✓
- Frontend templates ✓
- Automated tests ✓
- GitHub commits ✓

---

## 📱 Next Steps (If Continuing)

1. **Selenium UI Tests:** Automate booking flow, rating submission, alumni moderation
2. **Email Notifications:** Send booking confirmations, rating request emails
3. **Payment Integration:** Add payment for skills (not in current sprint)
4. **Mobile App:** React Native frontend (separate project)

---

## 🚢 Deployment Checklist

Before production:
- [ ] Set `DEBUG = False` in `settings.py`
- [ ] Configure actual MySQL database
- [ ] Set SMTP credentials for email
- [ ] Create a production superuser
- [ ] Run migrations on production DB
- [ ] Test all features on staging

---

**Sprint Summary:** All 5 backend features (UN-60, UN-64, UN-85, UN-69, UN-73) fully implemented, tested, and merged to `main`. Ready for demo tomorrow! 🎉
