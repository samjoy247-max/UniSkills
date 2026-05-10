# ⚡ QUICK START: UN-44 for Joy

**Read this first. Takes 5 minutes.**

---

## 📋 YOUR TASK
Implement Skill Post CRUD (Create, Read, Update, Delete)

**Files to touch:** 6 files  
**Time estimate:** 2 days  
**Team impact:** HIGH (others depend on this)

---

## ✅ BEFORE YOU START

- [ ] Clone done?
- [ ] MySQL running?
- [ ] `python backend/manage.py runserver` works?
- [ ] Read: `GIT_WORKFLOW.md` (understand git commands)
- [ ] Read: `UN-44_IMPLEMENTATION_CHECKLIST.md` (detailed guide)

---

## 🚀 STEP 0: Setup (5 minutes)

```bash
cd "d:\Code\Software Engineering Lab\Development UniSkills TEST\FINAL UX"

# Get latest code
git checkout develop
git pull origin develop

# Create your working branch
git checkout -b feature/UN-44-skill-crud

# Verify
git branch
# Should show: * feature/UN-44-skill-crud
```

**✓ DONE!** You're ready to code.

---

## 🔨 STEP 1: Create File (10 minutes)

Create new file: `backend/accounts/forms.py`

Copy full content from: `UN-44_IMPLEMENTATION_CHECKLIST.md` → Section "1️⃣ Create `accounts/forms.py`"

**Test it:**
```bash
cd backend
python manage.py shell
>>> from accounts.forms import SkillPostForm
# Should work (no error)
```

---

## ✏️ STEP 2: Modify student.py (20 minutes)

Edit file: `backend/accounts/user_management/student.py`

1. Add imports at TOP:
```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.forms import SkillPostForm
from accounts.models import SkillPost
```

2. Add 3 functions at END of file:
   - `create_skill_post(request)`
   - `edit_skill_post(request, post_id)`
   - `delete_skill_post(request, post_id)`

Copy from: `UN-44_IMPLEMENTATION_CHECKLIST.md` → Section "2️⃣ Modify `accounts/user_management/student.py`"

**Test it:**
```bash
python manage.py check
# Should pass
```

---

## 🔗 STEP 3: Add URLs (5 minutes)

Edit file: `backend/accounts/urls.py`

Add these 3 lines in the `urlpatterns` list:
```python
path('skill/create/', user_management.create_skill_post, name='create_skill_post'),
path('skill/<int:post_id>/edit/', user_management.edit_skill_post, name='edit_skill_post'),
path('skill/<int:post_id>/delete/', user_management.delete_skill_post, name='delete_skill_post'),
```

---

## 📄 STEP 4: Create Templates (15 minutes)

Create 3 new files in `backend/templates/`:

1. `create_skill_post.html`
2. `edit_skill_post.html`
3. `delete_skill_post_confirm.html`

Copy content from: `UN-44_IMPLEMENTATION_CHECKLIST.md` → Section "4️⃣, 5️⃣, 6️⃣"

---

## 🧪 STEP 5: Test Locally (30 minutes)

```bash
cd backend

# Check for errors
python manage.py check

# Start server
python manage.py runserver

# In browser: http://localhost:8000/login/
# Login: instructor1 / instructor123

# Test create: http://localhost:8000/skill/create/
# Fill form, click "Post Skill"

# Test edit: Find your skill, click "Edit"
# Modify, click "Update Skill"

# Test delete: Find your skill, click "Delete"
# Click "Yes, Delete"

# Verify all worked!
```

---

## 💾 STEP 6: Commit (5 minutes)

```bash
# See what changed
git status

# Stage all
git add .

# Commit with YOUR NAME
git commit -m "UN-44: Implement skill post CRUD (create/edit/delete) - Joy"

# Verify
git log --oneline -3
# Should show your commit at top
```

---

## 📤 STEP 7: Push (5 minutes)

```bash
# Before push: pull latest (in case someone else committed)
git pull origin develop
# Should say "Already up to date"

# Push your branch
git push origin feature/UN-44-skill-crud

# Verify on GitHub/GitLab website
# Should see your branch there
```

---

## 🔀 STEP 8: Merge to Develop (10 minutes)

```bash
# Switch to develop
git checkout develop

# Pull latest
git pull origin develop

# Merge your feature
git merge feature/UN-44-skill-crud

# Should say "Fast-forward" (no conflicts!)

# Push merged code
git push origin develop

# Delete your feature branch
git branch -d feature/UN-44-skill-crud
git push origin --delete feature/UN-44-skill-crud

# Verify
git log --oneline -3
# Should show your commits
```

---

## ✨ STEP 9: Notify Team (2 minutes)

Send message to **Shahin**:

```
✅ UN-44 COMPLETE!

Your turn for UN-48 (Skill Moderation)

To start:
git checkout develop
git pull origin develop
git checkout -b feature/UN-48-skill-moderation

See: UN-48_IMPLEMENTATION_CHECKLIST.md
```

---

## 📋 FILES YOU TOUCHED

```
✅ Created:
   - backend/accounts/forms.py
   - backend/templates/create_skill_post.html
   - backend/templates/edit_skill_post.html
   - backend/templates/delete_skill_post_confirm.html

✅ Modified:
   - backend/accounts/user_management/student.py
   - backend/accounts/urls.py
```

---

## ✅ SUCCESS CHECKLIST

Before saying "DONE":

- [ ] All 6 files created/modified
- [ ] Can create skill post
- [ ] Can edit skill post
- [ ] Can delete skill post
- [ ] Form validates correctly
- [ ] Database records created
- [ ] Committed with clear message
- [ ] Pushed to develop
- [ ] Notified next person

---

## 🐛 STUCK?

| Problem | Fix |
|---------|-----|
| `SkillPostForm not found` | Make sure you created `forms.py` |
| `403 error on edit/delete` | Logged in? As the skill creator? |
| `Database table doesn't exist` | Run `setup_database.bat` |
| `Import error` | Check imports at top of file |
| `Git conflict` | See: `SAFE_GIT_WORKFLOW.md` |

---

## 📚 REFERENCE DOCUMENTS

- `UN-44_IMPLEMENTATION_CHECKLIST.md` - Full detailed guide with code
- `GIT_WORKFLOW.md` - Git commands explained
- `SAFE_GIT_WORKFLOW.md` - Merge conflict prevention
- `SETUP_GUIDE.md` - Database setup

---

## ⏰ TIMELINE

**Tuesday:** Implement (Steps 1-5)  
**Wednesday:** Test & Commit (Steps 6-7)  
**Thursday:** Merge & Notify (Steps 8-9)  

**Total: 2 days**

---

## 🎯 REMEMBER

1. **Work only on feature branch** (not develop)
2. **Commit often** (every 1-2 hours)
3. **Test locally before committing**
4. **Clear commit messages with your name**
5. **Pull before pushing**
6. **Merge only after testing**
7. **Notify next person when done**

---

**Ready? Start with STEP 0! 🚀**

---

*Need more detail? See: `UN-44_IMPLEMENTATION_CHECKLIST.md`*
