## UniSkills Development Workflow - Serial Implementation

**Project:** UniSkills Platform  
**Framework:** Django 5.2.6  
**Database:** MySQL 5.7+ with PyMySQL  
**Team:** Joy (SJ), Maria (TM), Shahin, Esha  

---

## 📋 Phase 1: Skill Management System (Sprint 2)

**Goal:** Implement skill posting, moderation, search, and discovery features  
**Implementation Order:** Serial (one person at a time)

---

### **TASK 1: UN-44 - Create & Manage Skill Posts**
**Assigned to:** Joy (SJ)  
**Duration:** 2 days  
**Status:** 🔴 Not Started

#### What to implement:
- Create new skill post form (title, description, category, session mode, fee, time)
- Edit existing skill post
- Delete skill post with confirmation
- View my posted skills (dashboard list)
- Models: Already done in `accounts/models.py` (SkillPost model)

#### Files to create/modify:
```
accounts/user_management/student.py:
  ✏️ create_skill_post() - NEW function
  ✏️ edit_skill_post(post_id) - NEW function
  ✏️ delete_skill_post(post_id) - ALREADY DEFINED (check for duplicates)
  ✏️ SkillPostForm - NEW form class

accounts/urls.py:
  ✏️ Add routes for create/edit/delete if missing

templates/ (create if needed):
  ✏️ create_skill_post.html
  ✏️ edit_skill_post.html
  ✏️ delete_skill_post_confirm.html
```

#### Tests to verify:
- [ ] Can create skill post with all fields
- [ ] Form validates category choices (technical/non-technical/other)
- [ ] Session mode validated (online/offline/both)
- [ ] Post status defaults to "pending" (waiting moderation)
- [ ] Can edit own posts
- [ ] Can delete own posts
- [ ] Non-owners cannot edit/delete

#### After completion:
**Files to upload to git:**
- `accounts/user_management/student.py` (with new functions)
- `accounts/forms.py` or `accounts/user_management/forms.py` (SkillPostForm)
- `templates/create_skill_post.html`
- `templates/edit_skill_post.html`
- `templates/delete_skill_post_confirm.html`

**Git Commit:** From Joy's account  
```bash
git add accounts/user_management/student.py accounts/forms.py templates/
git commit -m "UN-44: Implement skill post CRUD - Joy"
git push origin develop
```

---

### **TASK 2: UN-48 - Skill Post Moderation**
**Assigned to:** Shahin  
**Duration:** 1 day  
**Status:** 🔴 Not Started  
**Depends on:** Task 1 (UN-44) completed

#### What to implement:
- Admin moderation dashboard (list pending posts)
- Approve skill post → status = "approved"
- Reject skill post → status = "rejected" + reason
- Moderation log tracking (SkillModerationLog model)

#### Files to create/modify:
```
accounts/user_management/admin_access.py or student.py:
  ✏️ moderation_dashboard() - ALREADY DEFINED (verify functionality)
  ✏️ moderate_skill_post(post_id, action) - ALREADY DEFINED
  ✏️ approve_skill_post(post_id) - if not in moderate_skill_post
  ✏️ reject_skill_post(post_id) - if not in moderate_skill_post

accounts/models.py:
  ✏️ SkillModerationLog - ALREADY DEFINED (verify)

templates/:
  ✏️ moderation_dashboard.html - NEW
  ✏️ moderate_skill_post.html - NEW (approve/reject form)
```

#### Tests to verify:
- [ ] Only admin/staff can access moderation
- [ ] Can see pending posts in dashboard
- [ ] Approve changes status to "approved"
- [ ] Reject changes status to "rejected" + stores reason
- [ ] Moderation log created automatically
- [ ] Moderator info stored in log

#### After completion:
**Files to upload to git:**
- `accounts/user_management/admin_access.py` or `student.py` (with moderation functions)
- `templates/moderation_dashboard.html`
- `templates/moderate_skill_post.html`

**Git Commit:** From Shahin's account  
```bash
git add accounts/user_management/ templates/
git commit -m "UN-48: Implement skill post moderation - Shahin"
git push origin develop
```

---

### **TASK 3: UN-52 - Search & Filter Skills**
**Assigned to:** Esha  
**Duration:** 1.5 days  
**Status:** 🔴 Not Started  
**Depends on:** Task 1 (UN-44) completed

#### What to implement:
- Search by keyword (title/description)
- Filter by category (technical/non-technical/other)
- Filter by session mode (online/offline/both)
- Save search filters for later (SkillSearchFilter model)
- Combine filters (category + mode + keyword)

#### Files to create/modify:
```
accounts/user_management/student.py:
  ✏️ skills_page() - ALREADY DEFINED (enhance with filters)
  ✏️ apply_keyword_filter() - ALREADY DEFINED
  ✏️ apply_category_filter() - ALREADY DEFINED
  ✏️ apply_mode_filter() - ALREADY DEFINED
  ✏️ save_search_filter() - NEW function
  ✏️ get_saved_filters() - NEW function

templates/:
  ✏️ skills.html - ALREADY EXISTS (update filters)
```

#### Tests to verify:
- [ ] Keyword search works (case-insensitive)
- [ ] Category filter works (returns only matching posts)
- [ ] Mode filter works (online/offline/both)
- [ ] Multiple filters work together
- [ ] Can save search filter
- [ ] Can load saved filters
- [ ] Only shows approved posts

#### After completion:
**Files to upload to git:**
- `accounts/user_management/student.py` (with filter functions)

**Git Commit:** From Esha's account  
```bash
git add accounts/user_management/student.py
git commit -m "UN-52: Add search and filter functionality - Esha"
git push origin develop
```

---

### **TASK 4: UN-56 - Browse Available Skills**
**Assigned to:** Maria (TM)  
**Duration:** 1.5 days  
**Status:** 🔴 Not Started  
**Depends on:** Task 1 (UN-44) + Task 2 (UN-48) completed

#### What to implement:
- Public skill browsing (only approved posts)
- Show available time slots (SkillSlot model)
- Display provider info, fee, session type
- Pagination (if many skills)
- Sort by: newest, price, rating

#### Files to create/modify:
```
accounts/user_management/student.py:
  ✏️ skills_page() - enhance display
  ✏️ skill_detail_page(post_id) - ALREADY DEFINED (verify)
  ✏️ get_available_slots(post_id) - NEW function
  ✏️ sort_skills(query, sort_by) - NEW function

accounts/models.py:
  ✏️ SkillSlot - ALREADY DEFINED (verify fields)

templates/:
  ✏️ skills.html - update layout for browsing
  ✏️ skill_detail.html - show slots, provider info
```

#### Tests to verify:
- [ ] Only approved posts visible
- [ ] Available time slots displayed
- [ ] Provider name/rating shown
- [ ] Can sort by price/date/rating
- [ ] Future dates only (not past slots)
- [ ] Shows available seat count

#### After completion:
**Files to upload to git:**
- `accounts/user_management/student.py` (with slot/sort functions)
- `templates/skill_detail.html` (if modified)

**Git Commit:** From Maria's account  
```bash
git add accounts/user_management/student.py templates/
git commit -m "UN-56: Implement skill browsing with slots - Maria"
git push origin develop
```

---

## 📋 Phase 2: Booking & Sessions (Sprint 3)

**Status:** ⏳ Scheduled after Phase 1

### **TASK 5: UN-60 - Booking Request Flow**
**Assigned to:** Joy (SJ)  
**Depends on:** Phase 1 complete  

### **TASK 6: UN-64 - Booking Status & History**
**Assigned to:** Joy (SJ)  
**Depends on:** Task 5 complete  

### **TASK 7: UN-69/73 - Rating System**
**Assigned to:** Esha  
**Depends on:** Tasks 5-6 complete  

---

## 📋 Phase 3: Alumni Features (Sprint 4)

**Status:** ⏳ Scheduled after Phase 2

### **TASK 8: UN-77 - Student & Alumni Registration**
**Status:** ✅ DONE (OTP integrated)

### **TASK 9: UN-81/82/83/85 - Alumni Posts**
**Assigned to:** Maria (TM)  
**Depends on:** Authentication working  

---

## 🔄 Git Workflow

### After each task:

**1. Pull latest changes:**
```bash
git fetch origin
git pull origin develop
```

**2. Create feature branch:**
```bash
git checkout -b feature/UN-XX-name
```

**3. Implement code**

**4. Test locally**

**5. Commit from assigned person's account:**
```bash
git add <files>
git commit -m "UN-XX: description - PersonName"
```

**6. Push:**
```bash
git push origin feature/UN-XX-name
```

**7. Create Pull Request (or notify for merge)**

**8. Next person pulls develop branch**

---

## 📦 Database Setup for Clone

When team members clone the repository:

**Windows:**
```bash
git clone <repo-url>
cd UniSkills
copy .env.example .env
# Edit .env with MySQL credentials
setup_database.bat
python backend/manage.py runserver
```

**Linux/Mac:**
```bash
git clone <repo-url>
cd UniSkills
cp .env.example .env
# Edit .env with MySQL credentials
chmod +x setup_database.sh
./setup_database.sh
python backend/manage.py runserver
```

---

## ✅ Verification Checklist

Before marking task complete:
- [ ] Code follows Django best practices
- [ ] All forms validate properly
- [ ] CSRF tokens on all POST forms
- [ ] Login required on protected views
- [ ] Proper error messages shown
- [ ] No duplicate functions
- [ ] Migrations work cleanly
- [ ] Test data can be created
- [ ] Git history is clean

---

## 🎯 Current Status Summary

| Task | Feature | Owner | Status |
|------|---------|-------|--------|
| UN-44 | Create Skill Posts | Joy (SJ) | 🔴 Not Started |
| UN-48 | Moderate Posts | Shahin | 🔴 Blocked (needs UN-44) |
| UN-52 | Search & Filter | Esha | 🔴 Blocked (needs UN-44) |
| UN-56 | Browse Skills | Maria (TM) | 🔴 Blocked (needs UN-44, UN-48) |
| UN-60 | Booking | Joy (SJ) | 🔴 Blocked (needs Phase 1) |
| UN-64 | History | Joy (SJ) | 🔴 Blocked (needs UN-60) |
| UN-69/73 | Ratings | Esha | 🔴 Blocked (needs UN-60+64) |
| UN-77 | Auth + OTP | — | ✅ DONE |
| UN-81/82/85 | Alumni | Maria (TM) | 🔴 Blocked (needs UN-77+moderation) |

---

## 📞 Communication

After each task completion, team member should report:
1. ✅ Task completed and tested
2. 📁 Files modified/created:
   - models.py
   - views/functions
   - forms
   - templates
   - urls
3. 🧪 Test cases verified
4. 📝 Commit hash and message
5. ⏭️ Ready for next person

---

*Last Updated: May 9, 2026*  
*Next Review: After UN-44 complete*
