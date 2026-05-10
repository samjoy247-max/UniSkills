# Safe Git Workflow - Serial Development (No Merge Conflicts)

## 🎯 GOAL
Each person does one task at a time, avoiding merge conflicts by following specific git workflow.

---

## ⚠️ THE PROBLEM WE'RE AVOIDING

```
Without safe workflow:
Joy edits student.py
Shahin edits student.py  ← CONFLICT!
Esha edits student.py     ← CONFLICT!
Maria edits student.py    ← CONFLICT!

Result: Merge conflicts nightmare!
```

---

## ✅ THE SOLUTION: SERIAL WORKFLOW

```
Joy edits student.py     → Merges to develop ✓
  ↓ (Wait for merge)
Shahin edits student.py  → Merges to develop ✓
  ↓ (Wait for merge)
Esha edits student.py    → Merges to develop ✓
  ↓ (Wait for merge)
Maria edits student.py   → Merges to develop ✓

Result: NO conflicts!
```

---

## 📋 THE RULES

### Rule 1: Only ONE Person Works at a Time
- Joy does UN-44 ONLY
- Shahin waits until UN-44 merged
- Then Shahin does UN-48 ONLY
- And so on...

### Rule 2: Always Create Feature Branch
- Never work on `develop` directly
- Always create: `feature/UN-XX-taskname`
- Keep `develop` clean

### Rule 3: Pull Before Working
- Before starting: `git pull origin develop`
- Gets latest code from others

### Rule 4: Commit Often & Early
- Don't work for 5 hours then commit
- Commit every 1-2 hours of work
- Smaller commits = easier to fix conflicts

### Rule 5: Merge to Develop Immediately
- After testing: merge feature → develop
- Don't let branch sit for days
- Fresh merge = no conflicts

---

## 🚀 STEP-BY-STEP: SAFE WORKFLOW

### **JOY'S TURN (UN-44)**

#### Day 1 Morning: Start

```bash
# Go to project folder
cd "d:\Code\Software Engineering Lab\Development UniSkills TEST\FINAL UX"

# Ensure on develop
git checkout develop

# Pull latest (get everyone's changes so far)
git pull origin develop

# Create feature branch (ALWAYS from develop)
git checkout -b feature/UN-44-skill-crud

# Verify you're on feature branch
git branch
# Output should be: * feature/UN-44-skill-crud
```

#### Day 1 Afternoon: First Commit

```bash
# Edit files: forms.py, student.py, urls.py, templates

# Check what changed
git status

# Stage changes
git add .

# Commit (include your name!)
git commit -m "UN-44: Add SkillPostForm and create_skill_post function - Joy"

# Push to keep backup
git push origin feature/UN-44-skill-crud
```

#### Day 2 Afternoon: Second Commit (After Testing)

```bash
# Edit templates: create_skill_post.html, edit_skill_post.html

# Check what changed
git status

# Stage changes
git add .

# Commit
git commit -m "UN-44: Add skill post templates - Joy"

# Push again
git push origin feature/UN-44-skill-crud
```

#### Day 2 End: Testing Complete, Ready to Merge

```bash
# Final check: all tests pass locally
python backend/manage.py runserver
# Test in browser: Create/Edit/Delete skill
# Verify: All working!

# Check final status
git status
# Should show: "nothing to commit, working tree clean"

# See all commits on feature branch
git log --oneline -5
# Should show your commits

# IMPORTANT: Before merging, pull latest develop
git pull origin develop

# If NO conflicts, continue to merge

# Switch to develop
git checkout develop

# Pull latest (in case someone else merged)
git pull origin develop

# Merge feature branch into develop
git merge feature/UN-44-skill-crud

# Verify merge successful
git log --oneline -5
# Should show your commits at top

# Push merged code to develop
git push origin develop

# Optional: Delete feature branch
git branch -d feature/UN-44-skill-crud
git push origin --delete feature/UN-44-skill-crud

# Notify next person
echo "UN-44 COMPLETE! Ready for UN-48. Shahin, your turn!"
```

---

### **SHAHIN'S TURN (UN-48) - Same Pattern**

```bash
# Wait for notification: "UN-44 merged to develop"

# Start fresh
git checkout develop
git pull origin develop

# Create Shahin's feature branch
git checkout -b feature/UN-48-skill-moderation

# Do your work (moderation functions, templates)

# Commit with your name
git commit -m "UN-48: Implement skill moderation dashboard - Shahin"

# Push feature branch
git push origin feature/UN-48-skill-moderation

# Test locally
python backend/manage.py runserver
# Test moderation: approve/reject skills

# Before merging: pull latest develop
git pull origin develop

# If no conflicts, merge
git checkout develop
git pull origin develop
git merge feature/UN-48-skill-moderation
git push origin develop

# Delete feature branch
git branch -d feature/UN-48-skill-moderation
git push origin --delete feature/UN-48-skill-moderation

# Notify next person
echo "UN-48 COMPLETE! Ready for UN-52. Esha, your turn!"
```

---

## 🚨 IF MERGE CONFLICTS HAPPEN

### **Scenario: Conflict During `git pull origin develop`**

```bash
# You see:
# error: Your local changes to the following files would be overwritten by merge:
#   backend/accounts/user_management/student.py

# SOLUTION:

# 1. Commit YOUR changes first
git status
git add .
git commit -m "UN-44: [your work] - Joy"

# 2. Try pull again
git pull origin develop

# 3. If conflict markers appear in student.py:
# <<<<<<< HEAD
# your code
# =======
# their code
# >>>>>>> origin/develop

# 4. Open file in editor, resolve conflict
# Keep what you want, DELETE conflict markers
# Save file

# 5. Mark as resolved
git add backend/accounts/user_management/student.py

# 6. Complete the merge
git commit -m "Resolve merge conflict in student.py"

# 7. Push
git push origin feature/UN-44-skill-crud
```

---

## 🛡️ PREVENTION: BEFORE EACH COMMIT

### **Checklist:**

```bash
# 1. Pull latest develop
git fetch origin
git pull origin develop

# 2. Check for conflicts in your files
git status
# Should NOT show "both added", "both modified", "both deleted"

# 3. Run Django checks
cd backend
python manage.py check

# 4. Run migrations dry-run
python manage.py makemigrations --dry-run

# 5. Start server, test manually
python manage.py runserver
# Test your feature in browser

# 6. If ALL GOOD, commit
git add .
git commit -m "UN-XX: [description] - YourName"

# 7. Push immediately
git push origin feature/UN-XX-taskname
```

---

## 📊 GIT COMMAND REFERENCE

| Command | What it does | When to use |
|---------|-------------|-----------|
| `git branch` | Show current branch | Check which branch you're on |
| `git checkout develop` | Switch to develop | Before pulling/merging |
| `git checkout -b feature/UN-XX` | Create new feature branch | Starting new task |
| `git pull origin develop` | Get latest from others | Before starting work |
| `git status` | Show changes | Before committing |
| `git add .` | Stage all changes | Before committing |
| `git commit -m "..."` | Save changes locally | After completing feature |
| `git push origin feature/UN-XX` | Upload to GitHub | After committing |
| `git merge feature/UN-XX` | Combine branches | When merging to develop |
| `git log --oneline` | Show commit history | Verify commits |

---

## ✅ DAILY CHECKLIST

### **Morning (If Your Turn):**
```bash
[ ] Pull latest: git pull origin develop
[ ] Create feature branch: git checkout -b feature/UN-XX-name
[ ] Verify branch: git branch
[ ] Ready to code!
```

### **After Each Change (Every Hour):**
```bash
[ ] Test locally: python manage.py runserver
[ ] Check: git status
[ ] Commit: git add . && git commit -m "UN-XX: [desc] - Name"
[ ] Push: git push origin feature/UN-XX-name
```

### **End of Day:**
```bash
[ ] All tests passing
[ ] All changes committed
[ ] Feature branch pushed
[ ] Code review done
[ ] Ready to merge
```

### **Merge Day:**
```bash
[ ] Pull latest develop: git pull origin develop
[ ] No conflicts?
[ ] Switch to develop: git checkout develop
[ ] Pull again: git pull origin develop
[ ] Merge feature: git merge feature/UN-XX-name
[ ] Push: git push origin develop
[ ] Delete feature branch
[ ] Notify next person!
```

---

## 🎯 EXAMPLE: PERFECT WORKFLOW

### **Joy's Perfect UN-44 Implementation**

**Tuesday 10 AM:**
```bash
git checkout develop
git pull origin develop
git checkout -b feature/UN-44-skill-crud
# Edit forms.py, add SkillPostForm
git add . && git commit -m "UN-44: Add SkillPostForm - Joy"
git push origin feature/UN-44-skill-crud
```

**Tuesday 3 PM:**
```bash
# Edit student.py, add create_skill_post()
git add . && git commit -m "UN-44: Add create_skill_post function - Joy"
git push origin feature/UN-44-skill-crud
```

**Wednesday 10 AM:**
```bash
# Test locally - all working!
# Edit templates
git add . && git commit -m "UN-44: Add skill post templates - Joy"
git push origin feature/UN-44-skill-crud
```

**Wednesday 4 PM (Merge Time):**
```bash
git pull origin develop      # Get any latest changes
# NO CONFLICTS! (because Shahin/Esha/Maria haven't touched this branch)

git checkout develop
git pull origin develop
git merge feature/UN-44-skill-crud
git push origin develop

git branch -d feature/UN-44-skill-crud
git push origin --delete feature/UN-44-skill-crud

# Notify Shahin: "UN-44 done! Your turn for UN-48"
```

**Result:** ✅ NO CONFLICTS, Clean git history!

---

## 🚫 WHAT NOT TO DO

```
❌ Work on develop directly
❌ Merge before testing
❌ Commit without message
❌ Work on someone else's branch
❌ Force push (-f flag)
❌ Delete commits after push
❌ Edit same file simultaneously with teammate
✅ Follow serial workflow
✅ Always test before merging
✅ Clear commit messages with name
✅ One person per task at a time
```

---

## 📞 HELP

| Problem | Solution |
|---------|----------|
| Lost on which branch? | `git branch` |
| Made wrong commits? | `git log --oneline` then decide |
| Conflict markers in file? | Open file, manually fix, `git add`, `git commit` |
| Accidental push to develop? | Contact team lead immediately |
| Feature branch won't delete? | `git branch -D feature/name` (force) |

---

## 🎓 WHY THIS WORKS

1. **One person at a time** = No file conflicts
2. **Feature branches** = develop stays clean
3. **Frequent pulls** = Stay updated
4. **Quick merges** = Less divergence
5. **Clear messages** = Easy to track

---

**Result: Zero merge conflicts, clean git history, happy team! 🎉**

Last Updated: May 9, 2026
