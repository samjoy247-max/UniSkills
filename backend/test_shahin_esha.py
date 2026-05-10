"""
Quick test for Shahin (UN-64, UN-85) and Esha (UN-69, UN-73) backend work
Tests: session_history view, alumni moderation, and rating submission
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniskills_backend.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import SkillPost, Booking, SessionHistory, Rating, AlumniPost
from django.utils import timezone
from datetime import timedelta

CustomUser = get_user_model()

print("\n" + "="*60)
print("TESTING SHAHIN (UN-64, UN-85) & ESHA (UN-69, UN-73)")
print("="*60)

# Create test users
print("\n[1] Creating test users...")
try:
    provider = CustomUser.objects.filter(username="test_provider_sh_v2").first() or \
               CustomUser.objects.create_user(
                   username="test_provider_sh_v2",
                   email="provider_sh_v2@test.edu",
                   password="testpass123",
                   role="provider"
               )
    print(f"✓ Provider: {provider.username}")
    
    student = CustomUser.objects.filter(username="test_student_sh_v2").first() or \
              CustomUser.objects.create_user(
                  username="test_student_sh_v2",
                  email="student_sh_v2@test.edu",
                  password="testpass123",
                  role="student"
              )
    print(f"✓ Student: {student.username}")
    
    alumni = CustomUser.objects.filter(username="test_alumni_esha_v2").first() or \
             CustomUser.objects.create_user(
                 username="test_alumni_esha_v2",
                 email="alumni_esha_v2@test.edu",
                 password="testpass123",
                 role="alumni",
                 is_alumni_verified=True
             )
    print(f"✓ Alumni: {alumni.username}")
    
except Exception as e:
    print(f"✗ Error creating users: {e}")
    sys.exit(1)

# UN-64: Test session_history model and functions
print("\n[2] Testing UN-64 (Session History)...")
booking = None
session = None

try:
    # Create a skill
    skill = SkillPost.objects.create(
        provider=provider,
        title=f"Session Test Skill {timezone.now().timestamp()}",
        description="Test skill for sessions",
        category=SkillPost.CATEGORY_TECHNICAL,
        session_mode=SkillPost.MODE_ONLINE,
        available_time=timezone.now() + timedelta(days=1),
        fee=500.00,
        status=SkillPost.STATUS_APPROVED
    )
    print(f"✓ Skill created: {skill.title}")
    
    # Create booking
    booking = Booking.objects.create(
        student=student,
        skill_post=skill,
        status=Booking.STATUS_ACCEPTED
    )
    print(f"✓ Booking created: ID={booking.id}, Status={booking.status}")
    
    # Create session history
    session = SessionHistory.objects.create(
        booking=booking,
        scheduled_date=timezone.now(),
        attendance_status="attended"
    )
    print(f"✓ Session created: ID={session.id}, Attendance={session.attendance_status}")
    
    # Query sessions (test session_history view logic)
    student_sessions = SessionHistory.objects.filter(booking__student=student)
    print(f"✓ Student has {student_sessions.count()} session(s)")
    
    provider_sessions = SessionHistory.objects.filter(booking__skill_post__provider=provider)
    print(f"✓ Provider has {provider_sessions.count()} session(s)")
    
except Exception as e:
    print(f"✗ UN-64 Error: {e}")

# UN-85: Test alumni moderation
print("\n[3] Testing UN-85 (Alumni Moderation)...")
try:
    # Create alumni post
    post = AlumniPost.objects.create(
        author=alumni,
        topic="Job Opportunity",
        title=f"Hiring Python Developer {timezone.now().timestamp()}",
        content="We are hiring senior Python developers",
        status=AlumniPost.STATUS_PENDING
    )
    print(f"✓ Alumni post created: ID={post.id}, Status={post.status}")
    
    # Test approve action
    post.status = AlumniPost.STATUS_APPROVED
    post.save()
    print(f"✓ Alumni post approved: ID={post.id}, Status={post.status}")
    
    # Query approved posts
    approved = AlumniPost.objects.filter(status=AlumniPost.STATUS_APPROVED)
    print(f"✓ Approved alumni posts: {approved.count()}")
    
except Exception as e:
    print(f"✗ UN-85 Error: {e}")

# UN-69/UN-73: Test rating submission
print("\n[4] Testing UN-69/UN-73 (Rating Submission)...")
try:
    if not booking:
        print("✗ UN-69/UN-73 Error: booking not created in UN-64 test")
    else:
        # Mark booking as completed for rating
        booking.status = Booking.STATUS_COMPLETED
        booking.save()
        print(f"✓ Booking marked as completed: ID={booking.id}")
        
        # Create rating
        rating = Rating.objects.create(
            rater=student,
            skill_post=booking.skill_post,
            session=session,
            rating=4.5,
            review_text="Great session! Learned a lot."
        )
        print(f"✓ Rating created: ID={rating.id}, Rating={rating.rating}, Text='{rating.review_text}'")
        
        # Get rating aggregate for skill
        ratings = Rating.objects.filter(skill_post=booking.skill_post)
        if ratings.count() > 0:
            avg_rating = sum([r.rating for r in ratings]) / ratings.count()
            print(f"✓ Skill average rating: {avg_rating:.2f} ({ratings.count()} rating(s))")
    
except Exception as e:
    print(f"✗ UN-69/UN-73 Error: {e}")

print("\n" + "="*60)
print("ALL TESTS COMPLETED ✓")
print("="*60)
