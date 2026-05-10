#!/bin/bash
# Database Setup Script for UniSkills
# Run this after cloning: ./setup_database.sh

echo "======================================"
echo "UniSkills Database Setup"
echo "======================================"

# Check if MySQL is running
echo "Checking MySQL connection..."
mysql -u root -e "SELECT 1" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "ERROR: MySQL is not running or root password is incorrect"
    echo "Please start MySQL service and update .env file"
    exit 1
fi

echo "✓ MySQL connection successful"

# Create database
echo "Creating database 'uniskills_test'..."
mysql -u root -e "DROP DATABASE IF EXISTS uniskills_test;"
mysql -u root -e "CREATE DATABASE uniskills_test CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
echo "✓ Database created"

# Run Django migrations
echo "Running Django migrations..."
cd "$(dirname "$0")/backend"
python manage.py migrate
echo "✓ Migrations complete"

# Load sample data
echo "Loading sample data..."
python manage.py loaddata sample_data.json 2>/dev/null || echo "No sample data fixture found (optional)"
echo "✓ Database setup complete!"

echo ""
echo "======================================"
echo "Setup Instructions:"
echo "1. Copy .env.example to .env"
echo "2. Update .env with your MySQL credentials"
echo "3. Run: python backend/manage.py runserver"
echo "4. Default test user: admin / admin"
echo "======================================"
