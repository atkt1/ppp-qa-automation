# Git Setup Guide - Private Repository

Complete guide to initialize Git and push to a private repository.

---

## 🎯 Quick Setup (5 Minutes)

### Option 1: Using the Setup Script (Easiest)

```bash
# Run the interactive setup script
./GIT_SETUP_COMMANDS.sh
```

The script will:
- ✅ Initialize Git
- ✅ Configure user
- ✅ Add files
- ✅ Create initial commit
- ✅ Add remote
- ✅ Push to repository

---

### Option 2: Manual Step-by-Step

#### Step 1: Initialize Git Repository

```bash
cd /Users/iamadi/Developer/Repos/ppMonoRepo

# Initialize Git
git init

# Verify
git status
```

**Expected output:**
```
Initialized empty Git repository in /Users/iamadi/Developer/Repos/ppMonoRepo/.git/
```

---

#### Step 2: Configure Git User

```bash
# Set your name and email
git config user.name "Your Name"
git config user.email "your.email@company.com"

# Verify
git config user.name
git config user.email
```

---

#### Step 3: Add Files to Git

```bash
# Add all files (respects .gitignore)
git add .

# Check what will be committed
git status

# You should see:
# - Python files (core/, team_alpha/)
# - Documentation (*.md files)
# - Configuration (Makefile, pytest.ini, pyproject.toml)
# - CI/CD (.gitlab-ci.yml)

# You should NOT see:
# - .venv/ (ignored)
# - __pycache__/ (ignored)
# - allure-results/ (ignored)
# - .env (ignored - contains secrets!)
```

---

#### Step 4: Create Initial Commit

```bash
git commit -m "Initial commit: QA Test Automation Framework

- Core framework with BasePage and BaseApiClient
- Team Alpha implementation (Google Shopping tests)
- Utility functions (string, wait, element helpers)
- Generic YAML data loader
- Parallel testing support with pytest-xdist
- Allure reporting integration
- Comprehensive documentation
- Makefile for common commands"
```

**Expected output:**
```
[main (root-commit) abc1234] Initial commit: QA Test Automation Framework
 XX files changed, XXXX insertions(+)
 create mode 100644 ...
```

---

#### Step 5: Rename Branch to 'main'

```bash
# Modern Git uses 'main' instead of 'master'
git branch -M main

# Verify
git branch
```

---

#### Step 6: Create Remote Repository

**⚠️ IMPORTANT: Make repository PRIVATE!**

##### For GitHub:

1. Go to https://github.com/new
2. **Repository name**: `qa-automation-framework`
3. **Description**: `Multi-team QA Test Automation Framework`
4. **Visibility**: **Private** ⚠️
5. **DO NOT** check "Initialize with README"
6. Click **Create repository**

##### For GitLab:

1. Go to https://gitlab.com/projects/new
2. **Project name**: `qa-automation-framework`
3. **Visibility**: **Private** ⚠️
4. **Uncheck** "Initialize with README"
5. Click **Create project**

##### For Company Git:

Ask your admin for the repository URL.

---

#### Step 7: Add Remote Origin

**For GitHub (HTTPS):**
```bash
git remote add origin https://github.com/YOUR_USERNAME/qa-automation-framework.git
```

**For GitHub (SSH - Recommended):**
```bash
git remote add origin git@github.com:YOUR_USERNAME/qa-automation-framework.git
```

**For GitLab (HTTPS):**
```bash
git remote add origin https://gitlab.com/YOUR_USERNAME/qa-automation-framework.git
```

**For GitLab (SSH - Recommended):**
```bash
git remote add origin git@gitlab.com:YOUR_USERNAME/qa-automation-framework.git
```

**For Company Git:**
```bash
git remote add origin <URL_FROM_YOUR_ADMIN>
```

**Verify:**
```bash
git remote -v
```

---

#### Step 8: Push to Remote

```bash
# Push to remote (first time)
git push -u origin main
```

**If using HTTPS, you'll be prompted for:**
- Username: `your_username`
- Password: `your_personal_access_token` (NOT your account password!)

**Expected output:**
```
Enumerating objects: XX, done.
Counting objects: 100% (XX/XX), done.
Delta compression using up to X threads
Compressing objects: 100% (XX/XX), done.
Writing objects: 100% (XX/XX), XX.XX KiB | XX.XX MiB/s, done.
Total XX (delta X), reused 0 (delta 0), pack-reused 0
To https://github.com/YOUR_USERNAME/qa-automation-framework.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

---

## 🔐 Authentication Setup

### Option A: Personal Access Token (HTTPS)

#### GitHub Token:

1. Go to https://github.com/settings/tokens
2. Click **Generate new token (classic)**
3. Name: `qa-automation-framework`
4. Select scopes: **repo** (all sub-options)
5. Click **Generate token**
6. **Copy token immediately** (you won't see it again!)
7. Use token as password when pushing

#### GitLab Token:

1. Go to https://gitlab.com/-/profile/personal_access_tokens
2. Name: `qa-automation-framework`
3. Scopes: **write_repository**
4. Click **Create personal access token**
5. **Copy token**
6. Use token as password when pushing

**Store credentials (so you don't enter token every time):**
```bash
# macOS
git config --global credential.helper osxkeychain

# Linux
git config --global credential.helper store

# Windows
git config --global credential.helper wincred
```

---

### Option B: SSH Keys (Recommended - More Secure)

#### Generate SSH Key (if you don't have one):

```bash
# Check if you already have SSH key
ls -la ~/.ssh/id_ed25519.pub

# If not, generate one
ssh-keygen -t ed25519 -C "your.email@company.com"

# Press Enter for default location
# Enter passphrase (optional but recommended)

# Copy public key to clipboard
cat ~/.ssh/id_ed25519.pub | pbcopy  # macOS
# Or display and copy manually:
cat ~/.ssh/id_ed25519.pub
```

#### Add SSH Key to GitHub:

1. Go to https://github.com/settings/keys
2. Click **New SSH key**
3. Title: `MacBook Pro` (or your device name)
4. Key type: **Authentication Key**
5. Paste your public key
6. Click **Add SSH key**

#### Add SSH Key to GitLab:

1. Go to https://gitlab.com/-/profile/keys
2. Paste your public key
3. Title: `MacBook Pro`
4. Click **Add key**

#### Test SSH Connection:

```bash
# Test GitHub
ssh -T git@github.com
# Expected: "Hi USERNAME! You've successfully authenticated..."

# Test GitLab
ssh -T git@gitlab.com
# Expected: "Welcome to GitLab, @USERNAME!"
```

---

## ✅ Verification Checklist

After pushing, verify:

- [ ] Repository is **PRIVATE** (check visibility settings)
- [ ] All files are pushed (check on GitHub/GitLab web interface)
- [ ] `.env` file is **NOT** pushed (should be in .gitignore)
- [ ] `allure-results/` is **NOT** pushed (should be in .gitignore)
- [ ] `__pycache__/` is **NOT** pushed (should be in .gitignore)
- [ ] Documentation is visible (README.md displays on main page)
- [ ] Commit message is clear and descriptive

**Check on GitHub/GitLab:**
```
Go to: https://github.com/YOUR_USERNAME/qa-automation-framework
or: https://gitlab.com/YOUR_USERNAME/qa-automation-framework

Should see:
✅ Private badge/icon
✅ All documentation files
✅ Core framework code
✅ Team Alpha tests
✅ README.md displayed
```

---

## 📝 Daily Git Workflow (After Initial Setup)

### Making Changes

```bash
# Check status
git status

# Add changed files
git add .
# Or specific files
git add file1.py file2.py

# Commit with message
git commit -m "Add new feature X"

# Push to remote
git push
```

### Pulling Latest Changes (if working in a team)

```bash
# Pull latest changes
git pull

# Or fetch and merge separately
git fetch
git merge origin/main
```

### Creating Feature Branches

```bash
# Create new branch
git checkout -b feature/new-test-suite

# Make changes and commit
git add .
git commit -m "Add new test suite"

# Push branch
git push -u origin feature/new-test-suite
```

---

## 🛡️ Repository Settings (Recommended)

### After Pushing, Configure:

1. **Add collaborators** (if working in a team):
   - GitHub: Settings → Collaborators → Add people
   - GitLab: Project Settings → Members → Invite member

2. **Branch protection** (optional but recommended):
   - Protect `main` branch
   - Require pull request reviews
   - Require status checks to pass

3. **Add repository description and topics**:
   - Topics: `playwright`, `pytest`, `test-automation`, `qa`, `python`

4. **Add CI/CD integration** (optional):
   - GitHub Actions or GitLab CI is already configured
   - Enable in repository settings

---

## 🐛 Troubleshooting

### Error: "Authentication failed"

**Solution:**
```bash
# If using HTTPS, use Personal Access Token as password (not account password)

# Or switch to SSH
git remote set-url origin git@github.com:YOUR_USERNAME/qa-automation-framework.git
```

### Error: "Repository not found"

**Solution:**
```bash
# Check remote URL
git remote -v

# Update if wrong
git remote set-url origin <CORRECT_URL>
```

### Error: "Permission denied (publickey)"

**Solution:**
```bash
# Test SSH connection
ssh -T git@github.com

# If fails, add SSH key to GitHub/GitLab (see SSH section above)

# Or use HTTPS instead
git remote set-url origin https://github.com/YOUR_USERNAME/qa-automation-framework.git
```

### Accidentally Pushed .env File

**DANGER:** .env contains secrets!

**Solution:**
```bash
# Remove from Git history
git rm --cached .env
git commit -m "Remove .env from repository"
git push

# Then regenerate all secrets/tokens in .env!
```

---

## 📚 Useful Git Commands

```bash
# Check status
git status

# See commit history
git log --oneline -10

# See changes
git diff

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes) - DANGER!
git reset --hard HEAD~1

# See all branches
git branch -a

# See remote info
git remote -v

# Pull latest
git pull

# Push changes
git push
```

---

## 🎉 Success!

You now have:
- ✅ Git repository initialized
- ✅ Initial commit created
- ✅ Code pushed to PRIVATE remote repository
- ✅ Ready for team collaboration
- ✅ Version control set up

**Repository URL:**
- GitHub: `https://github.com/YOUR_USERNAME/qa-automation-framework`
- GitLab: `https://gitlab.com/YOUR_USERNAME/qa-automation-framework`

---

## 📞 Next Steps

1. **Share with team** (add collaborators)
2. **Set up CI/CD** (already configured with .gitlab-ci.yml)
3. **Create feature branches** for new work
4. **Set up branch protection** for main branch
5. **Add project documentation** to repository wiki (optional)

---

**Created:** 2025-10-23
**Project:** QA Test Automation Framework
**Git Version:** 2.x+
