# UniSkills GitHub Push Guide - May 14, 2026

## 📋 Overview

The UniSkills backend is now on GitHub with individual feature branches for each team member:

- **Main Repo:** https://github.com/samjoy247-max/UniSkills
- **Owner:** samjoy247-max (Joy)
- **Main Branch:** `main` (stable)
- **Feature Branches:** 
  - `feature/shahin` (Shahin-100)
  - `feature/maria` (tanjidaMaria)
  - `feature/esha` (Ayat087)
  - `feature/joy` (samjoy247-max)

---

## 🔧 Setup Instructions (One-time)

### Step 1: Clone the Repository

```bash
cd d:\Code\Software\ Engineering\ Lab\Development\ UniSkills\ TEST
git clone https://github.com/samjoy247-max/UniSkills.git
cd UniSkills/backend
```

### Step 2: Switch to Your Feature Branch

```bash
# Shahin
git checkout feature/shahin

# Maria
git checkout feature/maria

# Esha
git checkout feature/esha

# Joy
git checkout feature/joy
```

### Step 3: Create a .gitconfig for Your Account (Optional - Recommended)

```bash
git config user.email "your-email@example.com"
git config user.name "Your GitHub Username"
```

---

## 📤 How to Push Your Work

### Option 1: Using Token in URL (Quick - One Push)

Replace `USERNAME`, `TOKEN`, and `BRANCH` with your info:

```bash
git add .
git commit -m "feat: your feature description"
git push https://USERNAME:TOKEN@github.com/samjoy247-max/UniSkills.git BRANCH
```

### Example for Shahin:

```bash
git add .
git commit -m "feat(UN-48): Add moderation quick actions"
git push https://Shahin-100:[REDACTED_TOKENS]@github.com/samjoy247-max/UniSkills.git feature/shahin
```

### Example for Maria:

```bash
git add .
git commit -m "feat(UN-56): Implement skill slot scheduling"
git push https://tanjidaMaria:[REDACTED_TOKENS]@github.com/samjoy247-max/UniSkills.git feature/maria
```

### Example for Esha:

```bash
git add .
git commit -m "feat(UN-52): Add advanced search filters"
git push https://Ayat087:[REDACTED_TOKENS]@github.com/samjoy247-max/UniSkills.git feature/esha
```

### Example for Joy:

```bash
git add .
git commit -m "feat(UN-44): Complete skill post CRUD"
git push origin feature/joy
```

---

## ✅ Commit Message Format

Use conventional commits for clarity:

```
feat(UN-##): Feature description          # New feature
fix(UN-##): Bug description               # Bug fix
docs(UN-##): Documentation update         # Documentation
test(UN-##): Test addition                # Tests
refactor(UN-##): Code refactoring         # Refactoring
```

### Examples:

```
feat(UN-48): Add bulk approve/reject actions for moderation
fix(UN-52): Fix search results pagination
docs(UN-44): Add skill post API documentation
test(UN-60): Add booking workflow tests
refactor(UN-56): Optimize slot allocation algorithm
```

---

## 🔍 Verify Your Push

### Check Remote Branches

```bash
git branch -a
# Should show:
#   feature/shahin
#   feature/maria
#   feature/esha
#   feature/joy
#   main
```

### View Your Commits

```bash
git log --oneline origin/feature/YOUR_BRANCH -5
```

### Check GitHub Status

Visit: https://github.com/samjoy247-max/UniSkills/branches

---

## ❌ Troubleshooting

### "Permission denied (publickey)"

Use HTTPS with token instead of SSH:
```bash
git push https://USERNAME:TOKEN@github.com/samjoy247-max/UniSkills.git BRANCH
```

### "fatal: Authentication failed"

Your token might be expired. Get a new one from GitHub:
1. Settings > Developer Settings > Personal Access Tokens
2. Generate new token with `repo` scope
3. Use new token in push command

### "Branch not found"

Verify you're on the correct branch:
```bash
git branch --show-current
git checkout feature/YOUR_BRANCH
```

### Merge Conflicts

If pulling from main causes conflicts:
```bash
git pull origin main
# Resolve conflicts manually
git add .
git commit -m "merge: resolve conflicts from main"
git push ...
```

---

## 📅 Recommended Workflow

1. **Create a feature branch locally** (if working on new feature)
   ```bash
   git checkout feature/YOUR_BRANCH
   git pull origin main  # Keep up to date
   ```

2. **Make your changes**
   ```bash
   # Edit files
   # Test locally
   # Commit small, logical chunks
   ```

3. **Commit frequently**
   ```bash
   git commit -m "feat(UN-##): Add feature X"
   git commit -m "fix(UN-##): Fix bug Y"
   ```

4. **Push regularly**
   ```bash
   git push https://USERNAME:TOKEN@github.com/samjoy247-max/UniSkills.git feature/YOUR_BRANCH
   ```

5. **Create Pull Request** (when ready to merge to main)
   - Go to GitHub
   - Click "New Pull Request"
   - Compare `main` ← `feature/YOUR_BRANCH`
   - Add description
   - Request review from team

---

## 🎯 Next Steps (After May 14 Pushes)

1. **All team members push to their feature branches**
2. **Joy reviews each feature branch**
3. **Create pull requests to merge into `main`**
4. **Final testing before deployment**

---

## 📞 Questions?

If you encounter issues:
1. Check this guide first
2. Ask in the team Slack/chat
3. Contact Joy (repo owner)

---

**Good luck! 🚀**
