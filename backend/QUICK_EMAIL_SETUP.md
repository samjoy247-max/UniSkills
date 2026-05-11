# QUICK SETUP: Enable Email Sending

## Your Current Issue
✅ OTP is being generated in the console  
❌ OTP is NOT being sent to Gmail

## Fix in 3 Steps:

### Step 1: Get Gmail App Password
1. Go to: https://myaccount.google.com/apppasswords
2. Select **Mail** and **Windows Computer**
3. Click **Generate** and copy the 16-character password

### Step 2: Update `.env` File
Edit: `backend/.env`

Change these three lines:
```
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=xxxx xxxx xxxx xxxx
DEFAULT_FROM_EMAIL=your_email@gmail.com
```

Example:
```
EMAIL_HOST_USER=samiul.joy@gmail.com
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
DEFAULT_FROM_EMAIL=samiul.joy@gmail.com
```

### Step 3: Restart Server
1. Stop the server (Ctrl+C in terminal)
2. Run: `python manage.py runserver 0.0.0.0:8000`
3. Register again → OTP will now be sent to your email!

## Note:
- The email can be sent to ANY address (23101102@uap-bd.edu, any Gmail, etc.)
- You just need to configure the SENDING email (EMAIL_HOST_USER) to be a Gmail account
- Users receiving the OTP can have any email address

## Testing:
After setup, register a new account and check your email inbox (and spam folder) for the OTP!
