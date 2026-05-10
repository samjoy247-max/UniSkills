# UniSkills Git Workflow Guide

## 🔧 Initial Setup (First Time Only)

### Configure Git for your account:
```bash
git config user.name "Your Full Name"
git config user.email "your.email@uap-bd.edu"

# Verify:
git config user.name
git config user.email
```

### Clone repository:
```bash
git clone <repository-url>
cd "Development UniSkills TEST\FINAL UX"
```

### Set up database and environment:
```bash
# Copy environment template
copy .env.example .env  (Windows)
cp .env.example .env    (Linux/Mac)

# Edit .env with your MySQL credentials

# Set up database
setup_database.bat      (Windows)
./setup_database.sh     (Linux/Mac)

# Install dependencies
pip install -r backend/requirements.txt

# Verify setup
python backend/manage.py runserver
# Visit http://localhost:8000 - should work
```

---

## 📋 Serial Development Workflow

### Each person works on ONE task at a time, in order:

**PHASE 1 - Do in this order:**
1. **Joy (SJ)** → UN-44 (Create Skill Posts)
2. **Shahin** → UN-48 (Moderation) 
3. **Esha** → UN-52 (Search & Filter)
4. **Maria (TM)** → UN-56 (Browse Skills)

---

## 🚀 Step-by-Step: How to Implement a Task

### **Step 1: Prepare Local Repository**

When it's your turn to work:

```bash
# Go to project root
cd "Development UniSkills TEST\FINAL UX"

# Ensure you have latest code
git fetch origin
git pull origin develop

# Create feature branch (use UN-XX from JIRA)
git checkout -b feature/UN-44-create-skill-posts
# Example for Shahin: feature/UN-48-skill-moderation
# Example for Esha: feature/UN-52-search-filter
# Example for Maria: feature/UN-56-browse-skills
```

### **Step 2: Implement Code**

Edit these files as needed for your task:
- `accounts/models.py` (if adding/modifying models)
- `accounts/forms.py` (if adding form validations)
- `accounts/user_management/student.py` or `alumni.py`
- `templates/*.html` (if adding/modifying templates)
- `accounts/urls.py` (if adding new routes)

Refer to `DEVELOPMENT_WORKFLOW.md` for specific files per task.

### **Step 3: Test Locally**

```bash
# Run migrations (if you modified models)
python backend/manage.py migrate

# Load test data (if needed)
python backend/manage.py shell < init_database.py

# Start server
python backend/manage.py runserver

# Test in browser: http://localhost:8000
# Test login with credentials from SETUP_GUIDE.md
# Test your implemented feature
```

### **Step 4: Check for Errors**

```bash
# Run migrations check
python backend/manage.py makemigrations --dry-run

# Check for syntax errors
python -m py_compile accounts/user_management/student.py

# Run Django checks
python backend/manage.py check
```

### **Step 5: Commit Your Changes**

```bash
# See all changes
git status

# Stage all changes
git add .
# Or stage specific files:
git add accounts/user_management/student.py
git add templates/create_skill_post.html
# etc.

# Commit with clear message
git commit -m "UN-44: Implement skill post CRUD - Joy"
# Format: "UN-XX: What you did - Your Name"

# Verify commit
git log --oneline -5
```

### **Step 6: Push to Remote**

```bash
# Push your branch
git push origin feature/UN-44-create-skill-posts

# Verify on GitHub/GitLab
# Should see your branch in repository
```

### **Step 7: Merge to Develop** 

Option A - Manual merge (if you have permission):
```bash
git checkout develop
git pull origin develop
git merge feature/UN-44-create-skill-posts
git push origin develop

# Delete feature branch (optional)
git branch -d feature/UN-44-create-skill-posts
git push origin --delete feature/UN-44-create-skill-posts
```

Option B - Create Pull Request (recommended):
- Go to GitHub/GitLab web interface
- Create Pull Request from `feature/UN-44-create-skill-posts` → `develop`
- Request review from team
- After approval, merge
- Delete branch

### **Step 8: Next Person Starts**

When task done and merged to develop:

Notify next person:
> UN-44 complete! Files updated:
> - accounts/models.py
> - accounts/user_management/student.py
> - accounts/forms.py
> - templates/create_skill_post.html
> 
> Ready for UN-48 (Shahin's turn)

Next person does:
```bash
git checkout develop
git pull origin develop
# ... their own implementation ...
```

---

## 📊 Files to Update Per Task

### **UN-44: Create Skill Posts (Joy)**
```
✏️ accounts/user_management/student.py
   - create_skill_post()
   - edit_skill_post()
   - delete_skill_post()

✏️ accounts/forms.py (or create new)
   - SkillPostForm

✏️ templates/
   - create_skill_post.html
   - edit_skill_post.html
   - delete_skill_post_confirm.html
   - (potentially modify skills.html)

✏️ accounts/urls.py
   - Add routes if not already there
```

### **UN-48: Skill Moderation (Shahin)**
```
✏️ accounts/user_management/admin_access.py or student.py
   - moderation_dashboard()
   - approve_skill_post()
   - reject_skill_post()

✏️ templates/
   - moderation_dashboard.html
   - moderate_skill_post.html
```

### **UN-52: Search & Filter (Esha)**
```
✏️ accounts/user_management/student.py
   - Enhance skills_page()
   - save_search_filter()
   - get_saved_filters()

✏️ templates/
   - Modify skills.html with filters
```

### **UN-56: Browse Skills (Maria)**
```
✏️ accounts/user_management/student.py
   - Enhance skills_page() for browsing
   - get_available_slots()
   - sort_skills()

✏️ templates/
   - Modify skills.html for browsing layout
   - Modify skill_detail.html to show slots
```

---

## 🔍 Common Git Commands

```bash
# See current branch
git branch

# See all branches
git branch -a

# Switch branch
git checkout develop
git checkout feature/UN-44-create-skill-posts

# See changes
git status
git diff

# See commits
git log --oneline -10

# Undo changes (before commit)
git checkout -- accounts/models.py

# Undo commits (careful!)
git reset --soft HEAD~1  # Undo last commit, keep changes
git reset --hard HEAD~1  # Undo last commit, discard changes

# Pull latest
git pull origin develop

# Push changes
git push origin feature/UN-44-create-skill-posts
```

---

## ⚠️ Conflict Resolution

If merge conflict occurs:

```bash
# See conflicting files
git status

# Open file in editor, see:
# <<<<<<< HEAD
# your code
# =======
# other code
# >>>>>>> other-branch

# Keep what you want, remove markers, save

# Mark as resolved
git add <conflicted-file>
git commit -m "Resolve merge conflict in <file>"
```

---

## ✅ Before Saying "Done"

Verify task completion:
- [ ] Code implemented and tested
- [ ] No duplicate functions
- [ ] No merge conflicts
- [ ] Database migrations work
- [ ] Test data loads
- [ ] Forms validate
- [ ] All required files committed
- [ ] Commit message is clear
- [ ] Code follows Django conventions

---

## 🎯 Task Transition Checklist

### When finishing a task:

```bash
# 1. Final commit
git status  # Should be clean
git commit -m "UN-XX: Final implementation - YourName"

# 2. Push to remote
git push origin feature/UN-XX-taskname

# 3. Merge to develop (or create PR)
git checkout develop
git pull origin develop
git merge feature/UN-XX-taskname
git push origin develop

# 4. Notify team
# "UN-XX Complete! Ready for UN-YY. Files: [list]"

# 5. Next person pulls
git checkout develop
git pull origin develop
```

---

## 📞 Need Help?

1. **Git issues?** → `git status`, `git log`
2. **Django issues?** → `python manage.py check`
3. **Database issues?** → Check `.env`, run `setup_database.bat`
4. **Lost changes?** → `git reflog` can help recover
5. **Merge conflicts?** → Edit conflicting files manually

---

**Always commit from your own account with your name in message!**

Last Updated: May 9, 2026
