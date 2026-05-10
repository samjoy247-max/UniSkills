# UN-52 Implementation Guide for Esha
## Search & Filter Skills

**Task Owner:** Esha  
**JIRA:** UN-52  
**Status:** ⏳ BLOCKED (Waiting for UN-44 complete)  
**Depends On:** UN-44 (Joy)  

---

## 📋 WHEN IT'S YOUR TURN

**You will start when:**
- [ ] Joy completes UN-44 and notifies Shahin
- [ ] Shahin completes UN-48 and notifies you
- [ ] develop branch has skill posts + moderation
- [ ] You can create/browse/filter approved skills

---

## 📁 FILES TO MODIFY

```
✏️ MODIFY:
  backend/accounts/user_management/student.py
  (Enhance existing skills_page() function)

🆕 CREATE OR MODIFY:
  backend/templates/skills.html (add filter UI)
```

---

## 🔨 WHAT YOU'LL BUILD

**Skill Search & Filter Page:**
- Keyword search (title/description)
- Category filter (technical/non-technical/other)
- Session mode filter (online/offline/both)
- Combine multiple filters
- Save search for later

**Functions to Implement/Enhance:**
- `skills_page()` - ALREADY EXISTS, add filter logic
- `apply_keyword_filter(queryset, keyword)` - Search
- `apply_category_filter(queryset, category)` - Category filter
- `apply_mode_filter(queryset, mode)` - Mode filter
- `save_search_filter()` - Save for later
- `get_saved_filters()` - Load saved filters

---

## ✅ BEFORE STARTING

When Shahin says "UN-48 done":

```bash
cd "d:\Code\Software Engineering Lab\Development UniSkills TEST\FINAL UX"

# Pull latest
git checkout develop
git pull origin develop

# Create your branch
git checkout -b feature/UN-52-search-filter

# Test: Can you see skill posts?
python backend/manage.py shell
>>> from accounts.models import SkillPost
>>> SkillPost.objects.filter(status='approved').count()
# Should show approved posts
```

---

## 🔍 IMPLEMENTATION HINT

**URL with filters example:**
```
/skills.html?keyword=django&category=technical&mode=online
```

**Your job:**
- Read GET params from request
- Filter database based on params
- Show filtered results
- Show filter UI in template

---

## 🧪 TESTING CHECKLIST

When implemented, verify:
- [ ] Keyword search finds skills (case-insensitive)
- [ ] Category filter works (only shows selected category)
- [ ] Mode filter works (online/offline/both)
- [ ] Multiple filters work together
- [ ] Can combine: keyword + category + mode
- [ ] Only approved posts shown
- [ ] Can save search filter
- [ ] Can load saved filters
- [ ] Empty search shows all approved posts

---

## 📤 WHEN COMPLETE

```bash
# Test locally
python backend/manage.py runserver

# Try filters:
# http://localhost:8000/skills.html?keyword=django
# http://localhost:8000/skills.html?category=technical
# http://localhost:8000/skills.html?mode=online

# Stage & commit
git add .
git commit -m "UN-52: Add search and filter functionality - Esha"

# Before pushing: pull latest
git pull origin develop

# Push
git push origin feature/UN-52-search-filter

# Merge to develop (or create PR)
# Notify Maria: "UN-52 done, your turn for UN-56"
```

---

## 🔗 DEPENDENT ON

- SkillPost model with status field
- Skills page already showing posts
- GET parameter handling in Django
- SkillSearchFilter model for saving

---

**Waiting for: Shahin to complete UN-48 ⏳**
