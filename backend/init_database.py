"""
Database initialization script for UniSkills
Run after migrations: python manage.py shell < init_database.py
"""

from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.models import ContentType
from accounts.models import CustomUser, SkillCategory, SkillPost
from datetime import datetime, timedelta
from decimal import Decimal
import os

def initialize_database():
    """Initialize database with required permissions and sample data"""
    
    print("=" * 60)
    print("UniSkills Database Initialization")
    print("=" * 60)
    
    # 1. Create user groups if they don't exist
    print("\n1. Creating user groups...")
    admin_group, _ = Group.objects.get_or_create(name="Admin")
    student_group, _ = Group.objects.get_or_create(name="Student")
    alumni_group, _ = Group.objects.get_or_create(name="Alumni")
    print(f"   ✓ Groups created: {[g.name for g in [admin_group, student_group, alumni_group]]}")
    
    # 2. Create test users
    print("\n2. Creating test users...")
    
    # Admin user
    admin_user, created = CustomUser.objects.get_or_create(
        username="admin",
        defaults={
            "email": "admin@uniskills.edu",
            "role": "student",
            "is_staff": True,
            "is_superuser": True,
            "department": "IT",
            "university_id": "ADM001",
        }
    )
    if created:
        admin_user.set_password("admin")
        admin_user.save()
        print(f"   ✓ Admin user created (admin/admin)")
    else:
        print(f"   • Admin user already exists")
    
    # Student test user
    student_user, created = CustomUser.objects.get_or_create(
        username="student1",
        defaults={
            "email": "student1@uap-bd.edu",
            "first_name": "Karim",
            "last_name": "Ahmed",
            "role": "student",
            "department": "CSE",
            "university_id": "CSE001",
            "is_alumni_verified": False,
        }
    )
    if created:
        student_user.set_password("student123")
        student_user.save()
        print(f"   ✓ Student user created (student1/student123)")
    else:
        print(f"   • Student user already exists")
    
    # Instructor user (also student but posts skills)
    instructor_user, created = CustomUser.objects.get_or_create(
        username="instructor1",
        defaults={
            "email": "instructor1@uap-bd.edu",
            "first_name": "Fatima",
            "last_name": "Khan",
            "role": "student",
            "department": "CSE",
            "university_id": "CSE002",
            "is_alumni_verified": False,
        }
    )
    if created:
        instructor_user.set_password("instructor123")
        instructor_user.save()
        print(f"   ✓ Instructor user created (instructor1/instructor123)")
    else:
        print(f"   • Instructor user already exists")
    
    # Alumni user
    alumni_user, created = CustomUser.objects.get_or_create(
        username="alumni1",
        defaults={
            "email": "alumni1@uap-bd.edu",
            "first_name": "Hassan",
            "last_name": "Rahman",
            "role": "alumni",
            "department": "CSE",
            "university_id": "CSE2020001",
            "graduation_year": 2020,
            "major": "Computer Science",
            "current_company": "TechCorp BD",
            "is_alumni_verified": True,
        }
    )
    if created:
        alumni_user.set_password("alumni123")
        alumni_user.save()
        print(f"   ✓ Alumni user created (alumni1/alumni123)")
    else:
        print(f"   • Alumni user already exists")
    
    # 3. Create skill categories
    print("\n3. Creating skill categories...")
    categories = [
        ("Web Development", "Learn HTML, CSS, JavaScript, React, Django"),
        ("Mobile Development", "iOS, Android, Flutter development"),
        ("Data Science", "Python, Machine Learning, Data Analysis"),
        ("Project Management", "Agile, Scrum, Leadership skills"),
        ("Communication", "Presentation, Writing, Negotiation"),
        ("Language", "English, Bengali, Arabic, Chinese"),
    ]
    
    created_categories = {}
    for name, desc in categories:
        cat, created = SkillCategory.objects.get_or_create(
            name=name,
            defaults={"description": desc}
        )
        created_categories[name] = cat
        if created:
            print(f"   ✓ Category created: {name}")
        else:
            print(f"   • Category exists: {name}")
    
    # 4. Create sample skill posts
    print("\n4. Creating sample skill posts...")
    
    sample_skills = [
        {
            "title": "Django REST API Development",
            "description": "Learn how to build scalable REST APIs using Django and Django REST Framework",
            "category": "Web Development",
            "session_mode": "online",
            "fee": Decimal("500.00"),
            "provider": instructor_user,
            "status": SkillPost.STATUS_APPROVED,
        },
        {
            "title": "React.js Fundamentals",
            "description": "Master React hooks, components, and state management",
            "category": "Web Development",
            "session_mode": "both",
            "fee": Decimal("400.00"),
            "provider": instructor_user,
            "status": SkillPost.STATUS_APPROVED,
        },
        {
            "title": "Python Machine Learning",
            "description": "Introduction to ML with scikit-learn and TensorFlow",
            "category": "Data Science",
            "session_mode": "online",
            "fee": Decimal("800.00"),
            "provider": admin_user,
            "status": SkillPost.STATUS_APPROVED,
        },
        {
            "title": "English Communication",
            "description": "Improve English speaking and presentation skills",
            "category": "Communication",
            "session_mode": "offline",
            "fee": Decimal("300.00"),
            "provider": alumni_user,
            "status": SkillPost.STATUS_PENDING,
        },
    ]
    
    for skill_data in sample_skills:
        skill_data["available_time"] = datetime.now() + timedelta(days=7)
        skill, created = SkillPost.objects.get_or_create(
            title=skill_data["title"],
            provider=skill_data["provider"],
            defaults=skill_data
        )
        if created:
            print(f"   ✓ Skill created: {skill.title} (Status: {skill.get_status_display()})")
        else:
            print(f"   • Skill exists: {skill.title}")
    
    print("\n" + "=" * 60)
    print("Database initialization complete!")
    print("=" * 60)
    print("\nTest Credentials:")
    print("-" * 60)
    print("Admin:       admin / admin")
    print("Student:     student1 / student123")
    print("Instructor:  instructor1 / instructor123")
    print("Alumni:      alumni1 / alumni123")
    print("-" * 60)
    print("\nNext steps:")
    print("1. python manage.py runserver")
    print("2. Visit http://localhost:8000/login/")
    print("3. Try different user roles")
    print("=" * 60)


if __name__ == "__main__":
    try:
        initialize_database()
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
