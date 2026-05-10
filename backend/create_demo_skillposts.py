import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','uniskills_backend.settings')
django.setup()
from accounts.models import CustomUser, SkillPost
from django.utils import timezone

# Create 3 approved skill posts for joy_student
user = CustomUser.objects.filter(username='joy_student').first()
if not user:
    raise SystemExit('joy_student not found')

for i in range(1,4):
    title = f"Demo Skill {i} - Advanced Python"
    sp, created = SkillPost.objects.get_or_create(
        provider=user,
        title=title,
        defaults={
            'description': 'Demo skill for screenshots',
            'category': 'technical',
            'session_mode': 'online',
            'available_time': timezone.now(),
            'fee': 100*i,
            'status': 'APPROVED'
        }
    )
    if created:
        print('Created:', sp.title)
    else:
        # ensure status approved
        sp.status = 'APPROVED'
        sp.save()
        print('Updated/exists:', sp.title)

print('\n✅ Demo skill posts ready for joy_student')