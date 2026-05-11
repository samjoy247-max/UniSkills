# Gmail OTP Email Setup Guide

## Steps to Enable Email Sending via Gmail

### 1. Get Your Gmail App Password

1. Go to https://myaccount.google.com/apppasswords
2. Sign in with your Google Account (if not already signed in)
3. Select **Mail** and **Windows Computer** (or your device)
4. Click **Generate**
5. Google will show you a 16-character app password
6. Copy this password (e.g., `xxxx xxxx xxxx xxxx`)

### 2. Update the `.env` File

Edit the `.env` file in the backend folder and update these lines:

```env
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=xxxx xxxx xxxx xxxx
DEFAULT_FROM_EMAIL=your_email@gmail.com
```

Replace:
- `your_email@gmail.com` with your actual Gmail address
- `xxxx xxxx xxxx xxxx` with the 16-character app password you just created

### 3. Restart the Django Server

Kill the current server (Ctrl+C) and restart it:

```bash
python manage.py runserver 0.0.0.0:8000
```

### 4. Test Email Sending

1. Register a new student account
2. Enter your email
3. The OTP should now be sent to your Gmail inbox (check spam folder if needed)

## Troubleshooting

### "SMTPAuthenticationError" or "Invalid credentials"
- Make sure you're using the **App Password**, not your regular Gmail password
- Verify the app password is copied correctly (remove spaces if needed)
- Ensure 2-Step Verification is enabled on your Google Account

### Emails not arriving
- Check your spam/junk folder
- Verify the Gmail address in `DEFAULT_FROM_EMAIL` matches `EMAIL_HOST_USER`
- Check if Gmail is blocking the app (allow less secure apps if needed)

### "SMTPNotSupportedError"
- Make sure `EMAIL_USE_TLS=True` is set in `.env`
- Verify `EMAIL_PORT=587` is correct

## Alternative: Use Console Backend (Dev Only)

If you want to see OTP in the console instead of sending emails during development:

Update `.env`:
```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

Then restart the server. OTP will be printed to the console when users register.
