"""
UN-88: User and Content Management
Content CRUD operations, flagging, moderation
"""

from django.db import models
from accounts.models import CustomUser, AlumniPost


class ContentFlag(models.Model):
    """UN-88: Track flagged content for moderation"""
    
    FLAG_REASONS = [
        ('spam', 'Spam'),
        ('inappropriate', 'Inappropriate Content'),
        ('harassment', 'Harassment'),
        ('misinformation', 'Misinformation'),
        ('other', 'Other'),
    ]
    
    post = models.ForeignKey(AlumniPost, on_delete=models.CASCADE, related_name='flags')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reason = models.CharField(max_length=20, choices=FLAG_REASONS)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
    resolution = models.CharField(max_length=20, choices=[('approved', 'Approved'), ('removed', 'Removed')], null=True, blank=True)
    
    class Meta:
        unique_together = ('post', 'user')
    
    def __str__(self):
        return f"{self.post.title} - {self.reason}"


def create_alumni_post_content(user, title, content):
    """UN-88: Create new alumni post"""
    post = AlumniPost.objects.create(
        author=user,
        title=title,
        content=content,
        status='pending'
    )
    return post


def update_alumni_post_content(post_id, title=None, content=None):
    """UN-88: Update alumni post (owner only)"""
    try:
        post = AlumniPost.objects.get(id=post_id)
        if title:
            post.title = title
        if content:
            post.content = content
        post.save()
        return post
    except AlumniPost.DoesNotExist:
        return None


def delete_alumni_post_content(post_id):
    """UN-88: Delete alumni post (owner only)"""
    try:
        post = AlumniPost.objects.get(id=post_id)
        post.delete()
        return True
    except AlumniPost.DoesNotExist:
        return False


def flag_content(post_id, user, reason, description=''):
    """UN-88: Flag content for moderation"""
    try:
        post = AlumniPost.objects.get(id=post_id)
        flag, created = ContentFlag.objects.get_or_create(
            post=post,
            user=user,
            defaults={'reason': reason, 'description': description}
        )
        return flag, created
    except AlumniPost.DoesNotExist:
        return None, False


def get_flagged_content(limit=10):
    """UN-88: Get list of flagged content for moderation"""
    return ContentFlag.objects.filter(resolved=False).select_related('post', 'user')[:limit]


def resolve_flag(flag_id, resolution):
    """UN-88: Resolve a content flag"""
    try:
        flag = ContentFlag.objects.get(id=flag_id)
        flag.resolved = True
        flag.resolution = resolution
        
        if resolution == 'removed':
            flag.post.status = 'rejected'
            flag.post.save()
        
        flag.save()
        return flag
    except ContentFlag.DoesNotExist:
        return None


def get_user_content(user, content_type='posts'):
    """UN-88: Get all content created by user"""
    if content_type == 'posts':
        return AlumniPost.objects.filter(author=user).order_by('-created_at')
    return []


def get_content_stats():
    """UN-88: Get content statistics"""
    return {
        'total_posts': AlumniPost.objects.count(),
        'pending_posts': AlumniPost.objects.filter(status='pending').count(),
        'approved_posts': AlumniPost.objects.filter(status='approved').count(),
        'rejected_posts': AlumniPost.objects.filter(status='rejected').count(),
        'flagged_content': ContentFlag.objects.filter(resolved=False).count(),
    }
