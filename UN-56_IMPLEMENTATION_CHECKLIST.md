# UN-56 Implementation Guide for Maria (TM)
## Browse Available Skills

**Task Owner:** Maria (TM)  
**JIRA:** UN-56  
**Status:** ⏳ BLOCKED (Waiting for UN-44 & UN-48 complete)  
**Depends On:** UN-44 (Joy) + UN-48 (Shahin)  

---

## 📋 WHEN IT'S YOUR TURN

**You will start when:**
- [ ] Joy completes UN-44 and notifies team
- [ ] Shahin completes UN-48 and notifies team
- [ ] Esha completes UN-52 and notifies you
- [ ] develop branch has: creation, moderation, search working
- [ ] You can browse and see approved skill posts

---

## 📁 FILES TO MODIFY

```
✏️ MODIFY:
  backend/accounts/user_management/student.py
  (Enhance skills_page() for browsing display)

✏️ MODIFY:
  backend/templates/skills.html
  (Better layout for browsing)

🆕 CREATE/MODIFY:
  backend/templates/skill_detail.html
  (Show skill details + available slots)
```

---

## 🔨 WHAT YOU'LL BUILD

**Skill Browsing Page:**
- Display approved skill posts
- Show provider info (name, rating)
- Show session details (type, fee, time)
- Display available slots
- Pagination (if many skills)
- Sort by: newest, price, rating

**Functions to Implement/Enhance:**
- `skills_page()` - Enhance for browsing
- `skill_detail_page(post_id)` - Show full details
- `get_available_slots(post_id)` - Show time slots
- `sort_skills(queryset, sort_by)` - Sort results

---

## ✅ BEFORE STARTING

When Esha says "UN-52 done":

```bash
cd "d:\Code\Software Engineering Lab\Development UniSkills TEST\FINAL UX"

# Pull latest
git checkout develop
git pull origin develop

# Create your branch
git checkout -b feature/UN-56-browse-skills

# Test: Can you see skill details?
python backend/manage.py shell
>>> from accounts.models import SkillPost, SkillSlot
>>> skill = SkillPost.objects.filter(status='approved').first()
>>> skill.slots.all()
# Should show available slots for skill
```

---

## 📊 DATA STRUCTURE

**Skill Details to Show:**
- Title, description
- Provider name (from CustomUser)
- Fee amount
- Session mode (online/offline)
- Category
- Available slots (times when available)
- Booking button (if slots available)

**Slot Information:**
- Start time / End time
- Max students
- Booked count
- Available seats

---

## 🧪 TESTING CHECKLIST

When implemented, verify:
- [ ] Only approved posts visible
- [ ] Provider name/info shown
- [ ] Session details clear
- [ ] Available slots displayed
- [ ] Shows available seat count
- [ ] Can sort by price/date
- [ ] Future dates only (no past slots)
- [ ] Clicking skill shows detail page
- [ ] Pagination works (if many skills)
- [ ] Can see "Book Now" button on slots

---

## 📤 WHEN COMPLETE

```bash
# Test locally
python backend/manage.py runserver

# Visit:
# http://localhost:8000/skills.html (browsing page)
# http://localhost:8000/skills/1/ (detail page)

# Try sorting:
# http://localhost:8000/skills.html?sort=price
# http://localhost:8000/skills.html?sort=date

# Stage & commit
git add .
git commit -m "UN-56: Implement skill browsing with slots - Maria"

# Before pushing: pull latest
git pull origin develop

# Push
git push origin feature/UN-56-browse-skills

# Merge to develop (or create PR)
# Notify team: "UN-56 done! Phase 1 complete"
```

---

## 🔗 DEPENDENT ON

- SkillPost model with status field
- SkillSlot model for time slots
- Moderation complete (approved posts)
- Search/filter working
- CustomUser provider info

---

## 🎯 PHASE 1 MILESTONE

When you complete UN-56:
- ✅ Students can post skills (UN-44)
- ✅ Admin can moderate (UN-48)
- ✅ Users can search (UN-52)
- ✅ Users can browse (UN-56)

**Next Phase:** UN-60 (Bookings) → Waiting for Joy again

---

**Waiting for: Esha to complete UN-52 ⏳**
