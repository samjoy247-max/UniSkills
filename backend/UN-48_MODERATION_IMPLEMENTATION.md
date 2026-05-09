UN-48: Admin Moderation System Implementation
=============================================

Developer: Shahin (Shahin-100)
Email: 23101084@uap-bd.edu
Date: May 9, 2026

FEATURES IMPLEMENTED:
✅ Admin moderation dashboard
✅ List pending skill posts
✅ Approve/reject functionality
✅ Rejection reason tracking
✅ Status change logging
✅ Moderation templates

CHANGES:
- accounts/user_management/student.py:
  * moderation_dashboard() - Lists pending posts
  * moderate_skill_post() - Handle approve/reject
  
- accounts/models.py:
  * Added rejection_reason field to SkillPost
  * Added SkillModerationLog model
  
- accounts/urls.py:
  * Added moderation routes
  
- templates/accounts/:
  * moderation_dashboard.html - Admin dashboard
  * moderate_skill_post.html - Review & decision form

PERMISSIONS:
- @staff_member_required on all moderation views
- Only admins can access moderation dashboard
- Ensures data security

TESTING:
- Tested approve workflow
- Tested reject workflow with reasons
- Verified permission checks
