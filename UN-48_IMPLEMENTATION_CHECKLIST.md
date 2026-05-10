# UN-48 Implementation Guide for Shahin
## Skill Post Moderation

**Task Owner:** Shahin  
**JIRA:** UN-48  
**Status:** ⏳ BLOCKED (Waiting for UN-44 complete)  
**Depends On:** UN-44 (Joy)  

---

## 📋 WHEN IT'S YOUR TURN

**You will start when:**
- [ ] Joy completes UN-44 and notifies you
- [ ] develop branch has latest skill posts feature
- [ ] You can see `SkillPostForm` in code

---

## 📁 FILES TO CREATE/MODIFY

```
✏️ MODIFY:
  backend/accounts/user_management/admin_access.py
  (or student.py if admin functions there)

🆕 CREATE:
  backend/templates/moderation_dashboard.html
  backend/templates/moderate_skill_post.html
```

---

## 🔨 WHAT YOU'LL BUILD

**Moderation Dashboard:** Admin-only page showing:
- List of pending skill posts
- Approve button
- Reject button with reason

**Functions to Implement:**
- `moderation_dashboard()` - List pending posts (check if already exists)
- `approve_skill_post(post_id)` - Set status to "approved"
- `reject_skill_post(post_id)` - Set status to "rejected" + reason
- Auto-create SkillModerationLog entry

---

## ✅ BEFORE STARTING

When Joy says "UN-44 done":

```bash
cd "d:\Code\Software Engineering Lab\Development UniSkills TEST\FINAL UX"

# Pull latest
git checkout develop
git pull origin develop

# Create your branch
git checkout -b feature/UN-48-skill-moderation

# Test: Can you import SkillPostForm?
python backend/manage.py shell
>>> from accounts.forms import SkillPostForm
# Should work (no error)
```

---

## 📄 DETAILED IMPLEMENTATION

**See attached:** `UN-48_DETAILED_CODE.md` (will be provided when your turn comes)

Or follow: `DEVELOPMENT_WORKFLOW.md` → UN-48 section

---

## 🧪 TESTING CHECKLIST

When implemented, verify:
- [ ] Only admin/staff can access /moderation.html
- [ ] Lists all pending posts
- [ ] Can approve post → status changes to "approved"
- [ ] Can reject post → shows rejection reason form
- [ ] Moderation log created automatically
- [ ] Moderator info stored in log
- [ ] Post creator notified (if email configured)

---

## 📤 WHEN COMPLETE

```bash
# Test everything locally first
python backend/manage.py runserver

# Stage & commit
git add .
git commit -m "UN-48: Implement skill post moderation - Shahin"

# Before pushing: pull latest
git pull origin develop

# Push
git push origin feature/UN-48-skill-moderation

# Merge to develop (or create PR)
# Notify Esha: "UN-48 done, your turn for UN-52"
```

---

## 🔗 DEPENDENT ON

- SkillPost model (with status field)
- SkillModerationLog model
- User authentication
- @staff_member_required decorator

---

**Waiting for: Joy to complete UN-44 ⏳**
