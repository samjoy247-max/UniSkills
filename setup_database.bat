@echo off
REM Database Setup Script for UniSkills (Windows)
REM Run this after cloning: setup_database.bat

echo ======================================
echo UniSkills Database Setup
echo ======================================
echo.

REM Check if MySQL is installed
where mysql >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: MySQL is not installed or not in PATH
    echo Please install MySQL and add it to system PATH
    pause
    exit /b 1
)

echo Checking MySQL connection...
mysql -u root -e "SELECT 1" >nul 2>nul
if errorlevel 1 (
    echo ERROR: MySQL connection failed
    echo Please verify MySQL is running and root password is correct
    echo Update .env file with correct credentials
    pause
    exit /b 1
)

echo ✓ MySQL connection successful
echo.

REM Create database
echo Creating database 'uniskills_test'...
mysql -u root -e "DROP DATABASE IF EXISTS uniskills_test;"
mysql -u root -e "CREATE DATABASE uniskills_test CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
echo ✓ Database created
echo.

REM Run Django migrations
echo Running Django migrations...
cd backend
python manage.py migrate
if errorlevel 1 (
    echo ERROR: Migration failed
    pause
    exit /b 1
)
cd ..
echo ✓ Migrations complete
echo.

REM Load sample data (optional)
echo Loading sample data...
python backend/manage.py loaddata sample_data.json 2>nul || (
    echo No sample data fixture found (optional - skipping)
)
echo ✓ Database setup complete!
echo.

echo ======================================
echo Setup Instructions:
echo 1. Copy .env.example to .env
echo 2. Update .env with your MySQL credentials
echo 3. Run: python backend/manage.py runserver
echo 4. Access: http://localhost:8000
echo ======================================
echo.
pause
