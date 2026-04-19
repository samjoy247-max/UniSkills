# UniSkills Backend (TEST)

This backend now includes the Monday demo scope for user management:

- Student registration/login/logout
- Alumni registration/login with admin verification gate
- Admin user management through Django admin
- MySQL database configuration

## Stack

- Django 5.2.6
- MySQL (via PyMySQL)

## Setup

1. Create and activate virtual environment.
2. Install dependencies:

	pip install -r requirements.txt

3. Create a `.env` file from `.env.example` and fill your MySQL credentials.
4. Create MySQL database (default name: `uniskills_test`).
5. Run migrations:

	python manage.py makemigrations
	python manage.py migrate

6. Create admin account:

	python manage.py createsuperuser

7. Run server:

	python manage.py runserver

## Main URLs

- `/` Landing page
- `/register/student/` Student registration (only `@uap-bd.edu`)
- `/register/alumni/` Alumni registration (verification required)
- `/login/` Login page
- `/dashboard/` User dashboard
- `/admin/` Admin panel

## Admin Tasks for Demo

1. Login to `/admin/` with superuser.
2. Open `Custom users`.
3. Verify alumni by setting `is_alumni_verified=True`.
4. Deactivate users using `is_active=False` when needed.
