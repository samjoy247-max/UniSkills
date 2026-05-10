import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','uniskills_backend.settings')
django.setup()
from accounts.models import CustomUser, SkillPost
from django.utils import timezone

# Ensure provider users exist
joy = CustomUser.objects.filter(username='joy_student').first()
esha = CustomUser.objects.filter(username='esha_student').first()
if not joy or not esha:
    raise SystemExit('Required users not found')

# Create a pending skill for moderation
pending_title = 'Pending Approval Demo - Please Review'
sp, created = SkillPost.objects.get_or_create(
    provider=joy,
    title=pending_title,
    defaults={
        'description': 'This is a pending skill for moderation tests',
        'category': 'technical',
        'session_mode': 'online',
        'available_time': timezone.now(),
        'fee': 200,
        'status': 'PENDING'
    }
)
print('Pending skill:', sp.title, 'created' if created else 'exists - set to PENDING')
if not created:
    sp.status = 'PENDING'
    sp.save()

# Create a searchable skill for Esha tests
search_title = 'UniSkillsDemoSearch Python Basics'
ss, created = SkillPost.objects.get_or_create(
    provider=joy,
    title=search_title,
    defaults={
        'description': 'Searchable demo skill for filtering tests',
        'category': 'technical',
        'session_mode': 'online',
        'available_time': timezone.now(),
        'fee': 150,
        'status': 'APPROVED'
    }
)
print('Searchable skill:', ss.title, 'created' if created else 'exists - set to APPROVED')
if not created:
    ss.status = 'APPROVED'
    ss.save()

print('\n✅ Pending and searchable demo skills ready')