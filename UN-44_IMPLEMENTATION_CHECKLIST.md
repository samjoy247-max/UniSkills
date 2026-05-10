# UN-44 Implementation Guide for Joy (SJ)
## Create & Manage Skill Posts

**Task Owner:** Joy (SJ)  
**JIRA:** UN-44  
**Duration:** 2 days  
**Start Date:** May 9, 2026  

---

## 📋 PRE-IMPLEMENTATION CHECKLIST

Before starting, verify:

- [ ] Repository cloned
- [ ] `.env.example` copied to `.env`
- [ ] MySQL credentials in `.env` correct
- [ ] Run: `setup_database.bat` (Windows) or `./setup_database.sh` (Linux/Mac)
- [ ] Test: `python backend/manage.py runserver` works
- [ ] Test: Can login with `instructor1 / instructor123`
- [ ] Read: `GIT_WORKFLOW.md` and understand git commands
- [ ] Read: `DEVELOPMENT_WORKFLOW.md` → UN-44 section

---

## 🔄 SAFE GIT WORKFLOW (Avoid Merge Conflicts)

### **Step 0: Before You Start**

```bash
# Go to project folder
cd "d:\Code\Software Engineering Lab\Development UniSkills TEST\FINAL UX"

# Ensure you're on develop branch
git branch
# Output should show: * develop (asterisk = current)

# If not on develop, switch:
git checkout develop

# Pull latest code (IMPORTANT!)
git pull origin develop
```

### **Step 1: Create Your Feature Branch**

```bash
# Create new branch from develop (MUST be from develop)
git checkout -b feature/UN-44-skill-crud

# Verify branch created
git branch
# Should show:
# * feature/UN-44-skill-crud
#   develop
#   main
```

**⚠️ KEY POINT:** Never modify `develop` directly! Always use feature branch.

---

## 📁 FILES TO CREATE/MODIFY

### **File List with Locations:**

```
✏️ MODIFY:
  backend/accounts/user_management/student.py      (Add 3 new functions)
  backend/accounts/urls.py                        (Add/verify 3 routes)

🆕 CREATE:
  backend/accounts/forms.py                       (Create SkillPostForm)
  backend/templates/create_skill_post.html        (New)
  backend/templates/edit_skill_post.html          (New)
  backend/templates/delete_skill_post_confirm.html (New)
```

---

## 🔨 IMPLEMENTATION DETAILS

### **1️⃣ Create `accounts/forms.py` (NEW FILE)**

Create this new file at: `backend/accounts/forms.py`

```python
from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser, SkillPost, SkillCategory


class StudentRegistrationForm(UserCreationForm):
    """Registration form for students"""
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'department', 'university_id', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@uap-bd.edu'):
            raise forms.ValidationError("Please use your university email (@uap-bd.edu)")
        return email


class SkillPostForm(forms.ModelForm):
    """Form for creating/editing skill posts"""
    
    category = forms.ChoiceField(
        choices=SkillPost.CATEGORY_CHOICES,
        help_text="Select skill category"
    )
    
    session_mode = forms.ChoiceField(
        choices=SkillPost.MODE_CHOICES,
        help_text="How will you conduct the session?"
    )
    
    available_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        help_text="When is your skill session available?"
    )
    
    fee = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0,
        help_text="Session fee in Taka (BDT)"
    )
    
    class Meta:
        model = SkillPost
        fields = ['title', 'description', 'category', 'session_mode', 'available_time', 'fee']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Advanced Django Development'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe your skill in detail...'
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'session_mode': forms.Select(attrs={'class': 'form-control'}),
            'available_time': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'fee': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '500.00'
            }),
        }
    
    def clean_available_time(self):
        from datetime import datetime, timedelta
        available_time = self.cleaned_data.get('available_time')
        if available_time and available_time < datetime.now():
            raise forms.ValidationError("Available time must be in the future")
        return available_time
    
    def clean_fee(self):
        fee = self.cleaned_data.get('fee')
        if fee and fee < 0:
            raise forms.ValidationError("Fee cannot be negative")
        return fee
```

---

### **2️⃣ Modify `accounts/user_management/student.py`**

Add these 3 functions to the file (append at the end before any closing):

```python
# ==================== SKILL POST CRUD (UN-44) ====================

def create_skill_post(request):
    """Create a new skill post (UN-44)"""
    if request.method == 'POST':
        form = SkillPostForm(request.POST)
        if form.is_valid():
            skill_post = form.save(commit=False)
            skill_post.provider = request.user
            skill_post.status = SkillPost.STATUS_PENDING  # Pending moderation
            skill_post.save()
            
            # Redirect to skills page with success message
            from django.contrib import messages
            messages.success(request, 'Skill post created! Waiting for moderation approval.')
            return redirect('skills_page')
    else:
        form = SkillPostForm()
    
    return render(request, 'create_skill_post.html', {
        'form': form,
        'page_title': 'Post a New Skill'
    })


def edit_skill_post(request, post_id):
    """Edit an existing skill post (UN-44)"""
    skill_post = get_object_or_404(SkillPost, id=post_id)
    
    # Only provider or admin can edit
    if request.user != skill_post.provider and not request.user.is_staff:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("You cannot edit this post")
    
    if request.method == 'POST':
        form = SkillPostForm(request.POST, instance=skill_post)
        if form.is_valid():
            skill_post = form.save(commit=False)
            skill_post.status = SkillPost.STATUS_PENDING  # Reset to pending for re-review
            skill_post.save()
            
            from django.contrib import messages
            messages.success(request, 'Skill post updated! Resubmitted for moderation.')
            return redirect('skills_page')
    else:
        form = SkillPostForm(instance=skill_post)
    
    return render(request, 'edit_skill_post.html', {
        'form': form,
        'skill_post': skill_post,
        'page_title': f'Edit: {skill_post.title}'
    })


def delete_skill_post(request, post_id):
    """Delete a skill post with confirmation (UN-44)"""
    skill_post = get_object_or_404(SkillPost, id=post_id)
    
    # Only provider or admin can delete
    if request.user != skill_post.provider and not request.user.is_staff:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("You cannot delete this post")
    
    if request.method == 'POST':
        skill_post.delete()
        
        from django.contrib import messages
        messages.success(request, 'Skill post deleted successfully')
        return redirect('skills_page')
    
    return render(request, 'delete_skill_post_confirm.html', {
        'skill_post': skill_post,
        'page_title': 'Confirm Delete'
    })
```

**⚠️ IMPORTANT:** Add these imports at TOP of `student.py`:

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.forms import SkillPostForm
from accounts.models import SkillPost
```

---

### **3️⃣ Modify `accounts/urls.py`**

Add these URL patterns (add at the end of the file in the urlpatterns list):

```python
# UN-44: Skill Post CRUD
path('skill/create/', user_management.create_skill_post, name='create_skill_post'),
path('skill/<int:post_id>/edit/', user_management.edit_skill_post, name='edit_skill_post'),
path('skill/<int:post_id>/delete/', user_management.delete_skill_post, name='delete_skill_post'),
```

Verify the file has this import at top:
```python
from accounts import user_management
```

---

### **4️⃣ Create Template: `templates/create_skill_post.html`** (NEW FILE)

```html
{% extends 'base.html' %}
{% load static %}

{% block title %}Post a New Skill - UniSkills{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row">
        <div class="col-md-8 offset-md-2">
            <h2>{{ page_title }}</h2>
            <hr>
            
            {% if messages %}
                {% for message in messages %}
                    <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}
            
            <form method="post" class="needs-validation">
                {% csrf_token %}
                
                <div class="mb-3">
                    <label for="id_title" class="form-label">Skill Title *</label>
                    {{ form.title }}
                    {% if form.title.errors %}
                        <div class="text-danger small">{{ form.title.errors }}</div>
                    {% endif %}
                </div>
                
                <div class="mb-3">
                    <label for="id_description" class="form-label">Description *</label>
                    {{ form.description }}
                    {% if form.description.errors %}
                        <div class="text-danger small">{{ form.description.errors }}</div>
                    {% endif %}
                </div>
                
                <div class="row">
                    <div class="col-md-6 mb-3">
                        <label for="id_category" class="form-label">Category *</label>
                        {{ form.category }}
                        {% if form.category.errors %}
                            <div class="text-danger small">{{ form.category.errors }}</div>
                        {% endif %}
                    </div>
                    
                    <div class="col-md-6 mb-3">
                        <label for="id_session_mode" class="form-label">Session Mode *</label>
                        {{ form.session_mode }}
                        {% if form.session_mode.errors %}
                            <div class="text-danger small">{{ form.session_mode.errors }}</div>
                        {% endif %}
                    </div>
                </div>
                
                <div class="row">
                    <div class="col-md-6 mb-3">
                        <label for="id_available_time" class="form-label">Available Time *</label>
                        {{ form.available_time }}
                        {% if form.available_time.errors %}
                            <div class="text-danger small">{{ form.available_time.errors }}</div>
                        {% endif %}
                    </div>
                    
                    <div class="col-md-6 mb-3">
                        <label for="id_fee" class="form-label">Fee (BDT) *</label>
                        {{ form.fee }}
                        {% if form.fee.errors %}
                            <div class="text-danger small">{{ form.fee.errors }}</div>
                        {% endif %}
                    </div>
                </div>
                
                <div class="mt-4">
                    <button type="submit" class="btn btn-primary">Post Skill</button>
                    <a href="{% url 'skills_page' %}" class="btn btn-secondary">Cancel</a>
                </div>
            </form>
            
            <div class="alert alert-info mt-4">
                <strong>Note:</strong> Your skill post will be pending approval. Admins will review and approve/reject your post.
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

---

### **5️⃣ Create Template: `templates/edit_skill_post.html`** (NEW FILE)

```html
{% extends 'base.html' %}
{% load static %}

{% block title %}Edit Skill - UniSkills{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row">
        <div class="col-md-8 offset-md-2">
            <h2>{{ page_title }}</h2>
            <p class="text-muted">Original Status: <span class="badge bg-warning">{{ skill_post.get_status_display }}</span></p>
            <hr>
            
            {% if messages %}
                {% for message in messages %}
                    <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}
            
            <form method="post" class="needs-validation">
                {% csrf_token %}
                
                <div class="mb-3">
                    <label for="id_title" class="form-label">Skill Title *</label>
                    {{ form.title }}
                    {% if form.title.errors %}
                        <div class="text-danger small">{{ form.title.errors }}</div>
                    {% endif %}
                </div>
                
                <div class="mb-3">
                    <label for="id_description" class="form-label">Description *</label>
                    {{ form.description }}
                    {% if form.description.errors %}
                        <div class="text-danger small">{{ form.description.errors }}</div>
                    {% endif %}
                </div>
                
                <div class="row">
                    <div class="col-md-6 mb-3">
                        <label for="id_category" class="form-label">Category *</label>
                        {{ form.category }}
                        {% if form.category.errors %}
                            <div class="text-danger small">{{ form.category.errors }}</div>
                        {% endif %}
                    </div>
                    
                    <div class="col-md-6 mb-3">
                        <label for="id_session_mode" class="form-label">Session Mode *</label>
                        {{ form.session_mode }}
                        {% if form.session_mode.errors %}
                            <div class="text-danger small">{{ form.session_mode.errors }}</div>
                        {% endif %}
                    </div>
                </div>
                
                <div class="row">
                    <div class="col-md-6 mb-3">
                        <label for="id_available_time" class="form-label">Available Time *</label>
                        {{ form.available_time }}
                        {% if form.available_time.errors %}
                            <div class="text-danger small">{{ form.available_time.errors }}</div>
                        {% endif %}
                    </div>
                    
                    <div class="col-md-6 mb-3">
                        <label for="id_fee" class="form-label">Fee (BDT) *</label>
                        {{ form.fee }}
                        {% if form.fee.errors %}
                            <div class="text-danger small">{{ form.fee.errors }}</div>
                        {% endif %}
                    </div>
                </div>
                
                <div class="mt-4">
                    <button type="submit" class="btn btn-primary">Update Skill</button>
                    <a href="{% url 'skills_page' %}" class="btn btn-secondary">Cancel</a>
                </div>
            </form>
            
            <div class="alert alert-warning mt-4">
                <strong>Note:</strong> Editing will reset status to "Pending". Admin review required again.
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

---

### **6️⃣ Create Template: `templates/delete_skill_post_confirm.html`** (NEW FILE)

```html
{% extends 'base.html' %}
{% load static %}

{% block title %}Confirm Delete - UniSkills{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row">
        <div class="col-md-6 offset-md-3">
            <div class="card border-danger">
                <div class="card-body">
                    <h3 class="card-title text-danger">{{ page_title }}</h3>
                    <hr>
                    
                    <p><strong>Skill:</strong> {{ skill_post.title }}</p>
                    <p><strong>Category:</strong> {{ skill_post.get_category_display }}</p>
                    <p><strong>Status:</strong> <span class="badge bg-secondary">{{ skill_post.get_status_display }}</span></p>
                    
                    <div class="alert alert-danger mt-3">
                        <strong>⚠️ Warning:</strong> This action cannot be undone. All associated data (bookings, history) may be affected.
                    </div>
                    
                    <form method="post" class="mt-4">
                        {% csrf_token %}
                        <button type="submit" class="btn btn-danger btn-lg">
                            Yes, Delete This Skill
                        </button>
                        <a href="{% url 'skills_page' %}" class="btn btn-secondary btn-lg">
                            Cancel
                        </a>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

---

## ✅ IMPLEMENTATION CHECKLIST

After modifying all files:

- [ ] File `accounts/forms.py` created with SkillPostForm
- [ ] File `accounts/user_management/student.py` modified with 3 functions
- [ ] File `accounts/urls.py` modified with 3 routes
- [ ] Template `templates/create_skill_post.html` created
- [ ] Template `templates/edit_skill_post.html` created
- [ ] Template `templates/delete_skill_post_confirm.html` created
- [ ] All imports added to files
- [ ] No syntax errors in Python files
- [ ] Bootstrap classes in templates (if using Bootstrap)

---

## 🧪 LOCAL TESTING (Before Committing)

### **Test 1: Run migrations**
```bash
cd backend
python manage.py makemigrations --dry-run
# Should show no new migrations needed

python manage.py check
# Should show all checks passed
```

### **Test 2: Start server**
```bash
python manage.py runserver
```

### **Test 3: Test in browser**

1. **Login as instructor:**
   - Go to: http://localhost:8000/login/
   - Username: `instructor1`
   - Password: `instructor123`

2. **Create skill post:**
   - Click: "Post a Skill" or go to `/skill/create/`
   - Fill form:
     - Title: "Django Basics"
     - Description: "Learn Django fundamentals"
     - Category: "Technical" or "Web Development"
     - Mode: "Online"
     - Time: Select future date/time
     - Fee: "500"
   - Click: "Post Skill"
   - Verify: Success message shown, redirected to skills page

3. **Edit skill post:**
   - Find your posted skill
   - Click: "Edit"
   - Modify title: "Django Basics - Advanced"
   - Click: "Update Skill"
   - Verify: Success message shown

4. **Delete skill post:**
   - Find your skill
   - Click: "Delete"
   - Verify: Confirmation page shown
   - Click: "Yes, Delete"
   - Verify: Skill deleted, redirected

### **Test 4: Check database**
```bash
# Open Django shell
python manage.py shell

# Check skill posts created
>>> from accounts.models import SkillPost
>>> SkillPost.objects.all()
# Should show your created skills

>>> SkillPost.objects.filter(provider__username='instructor1')
# Should show only instructor1's skills

# Check status
>>> skill = SkillPost.objects.first()
>>> skill.status
# Should show 'pending'
```

---

## 🐛 TROUBLESHOOTING

| Error | Fix |
|-------|-----|
| `SkillPostForm not found` | Ensure `accounts/forms.py` created and imported correctly |
| `403 Forbidden on edit/delete` | Verify you're logged in as the skill creator |
| `DateTime field not working` | Ensure template uses `type="datetime-local"` in input |
| `CSRF token missing` | Verify `{% csrf_token %}` in all POST forms |
| `No module named 'forms'` | Add `from accounts.forms import SkillPostForm` to student.py |

---

## 📤 COMMITTING & PUSHING (After Testing)

### **Step 1: Check what changed**
```bash
# Go to project root
cd "d:\Code\Software Engineering Lab\Development UniSkills TEST\FINAL UX"

# See all changes
git status
```

Expected output:
```
modified:   backend/accounts/user_management/student.py
modified:   backend/accounts/urls.py
??         backend/accounts/forms.py
??         backend/templates/create_skill_post.html
??         backend/templates/edit_skill_post.html
??         backend/templates/delete_skill_post_confirm.html
```

### **Step 2: Stage files**

```bash
# Stage all files
git add .

# Or stage specific files
git add backend/accounts/forms.py
git add backend/accounts/user_management/student.py
git add backend/accounts/urls.py
git add backend/templates/create_skill_post.html
git add backend/templates/edit_skill_post.html
git add backend/templates/delete_skill_post_confirm.html
```

### **Step 3: Verify staged files**
```bash
git status
# Should show all files in green with "Changes to be committed:"
```

### **Step 4: Commit**
```bash
git commit -m "UN-44: Implement skill post CRUD (create/edit/delete) - Joy"
```

Format: `"UN-XX: Description - YourName"`

### **Step 5: Verify commit**
```bash
git log --oneline -5
# Should show your commit at top
```

Example:
```
a1b2c3d UN-44: Implement skill post CRUD (create/edit/delete) - Joy
f4e5d6c Fixed merge conflicts in models.py
...
```

---

## 🔄 PULLING BEFORE PUSHING (Avoid Conflicts)

### **Step 1: Before pushing, pull latest**

```bash
# Make sure all changes committed
git status
# Output should be: "nothing to commit, working tree clean"

# Pull latest from develop
git pull origin develop

# If no conflicts, continue to step 2
```

### **Step 2: If NO conflicts**

```bash
# Push your feature branch
git push origin feature/UN-44-skill-crud

# Verify on GitHub/GitLab - should see your branch
```

### **Step 3: If merge conflicts appear**

```bash
# STOP! Don't panic
# See conflicting files
git status

# Each file with <<<<<<< marks needs manual fix
# Open file, find:
# <<<<<<< HEAD
# your changes
# =======
# other changes
# >>>>>>> develop

# KEEP what you want, DELETE conflict markers
# Save file

# Mark as resolved
git add <fixed-file>

# Commit the merge
git commit -m "Resolve merge conflict in <filename>"

# Push again
git push origin feature/UN-44-skill-crud
```

---

## ✨ AFTER PUSHING: What's Next?

### **Option A: Manual Merge (If You Have Permission)**

```bash
# Switch to develop
git checkout develop

# Pull latest
git pull origin develop

# Merge your feature
git merge feature/UN-44-skill-crud

# Push to develop
git push origin develop

# Delete feature branch
git branch -d feature/UN-44-skill-crud
git push origin --delete feature/UN-44-skill-crud
```

### **Option B: Pull Request (Recommended)**

1. Go to GitHub/GitLab web interface
2. Click: "Create Pull Request"
3. Select: `feature/UN-44-skill-crud` → `develop`
4. Add description of changes
5. Request team review
6. After approval, click "Merge"
7. GitHub deletes branch automatically

---

## 📝 HANDOFF CHECKLIST (When Done)

Before notifying Shahin for UN-48:

- [ ] All tests passed locally
- [ ] Committed with clear message
- [ ] Pushed to feature branch
- [ ] Merged to develop (or PR created)
- [ ] develop branch updated with latest
- [ ] No outstanding changes
- [ ] Next person can pull and get latest code

### **Notification Message to Shahin:**

```
UN-44 COMPLETE! ✅

Files Updated:
- backend/accounts/forms.py (NEW)
- backend/accounts/user_management/student.py
- backend/accounts/urls.py
- backend/templates/create_skill_post.html (NEW)
- backend/templates/edit_skill_post.html (NEW)
- backend/templates/delete_skill_post_confirm.html (NEW)

What's Working:
✓ Create skill post
✓ Edit skill post
✓ Delete skill post with confirmation
✓ Form validation
✓ Posts default to "pending" status

Ready for UN-48 (Shahin)

To start:
git checkout develop
git pull origin develop
git checkout -b feature/UN-48-skill-moderation
```

---

## 🎯 SUCCESS CRITERIA

Task UN-44 is complete when:

- ✅ Can create new skill post (pending approval)
- ✅ Can edit own skill posts (resets to pending)
- ✅ Can delete own skill posts
- ✅ Form validates all fields
- ✅ Only owner/admin can edit/delete
- ✅ Database records created correctly
- ✅ No duplicate functions
- ✅ All 6 files committed and pushed

---

**Ready to start? Confirm by replying: "Ready Joy, start UN-44"**

Next: Shahin will do UN-48 (moderation) → Uses these new skill posts
