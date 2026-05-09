from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import CustomUser, SkillPost


class SkillSearchFilterTests(TestCase):
    def setUp(self):
        self.student = CustomUser.objects.create_user(
            username="student1",
            email="23101084@uap-bd.edu",
            password="Pass12345!",
            role="student",
        )
        self.provider_1 = CustomUser.objects.create_user(
            username="joy",
            email="joy@uap-bd.edu",
            password="Pass12345!",
            role="student",
        )
        self.provider_2 = CustomUser.objects.create_user(
            username="esha",
            email="esha@uap-bd.edu",
            password="Pass12345!",
            role="student",
        )

        now = timezone.now() + timedelta(days=1)

        self.python_post = SkillPost.objects.create(
            provider=self.provider_1,
            title="Python for Beginners",
            description="Start coding with python basics",
            category=SkillPost.CATEGORY_TECHNICAL,
            session_mode=SkillPost.MODE_ONLINE,
            available_time=now,
            fee=300,
            status=SkillPost.STATUS_APPROVED,
        )
        self.figma_post = SkillPost.objects.create(
            provider=self.provider_2,
            title="Figma UI Design",
            description="Learn wireframing and UI components",
            category=SkillPost.CATEGORY_NON_TECHNICAL,
            session_mode=SkillPost.MODE_OFFLINE,
            available_time=now,
            fee=200,
            status=SkillPost.STATUS_APPROVED,
        )
        SkillPost.objects.create(
            provider=self.provider_2,
            title="Hidden Pending Skill",
            description="Should not be shown in public list",
            category=SkillPost.CATEGORY_OTHER,
            session_mode=SkillPost.MODE_BOTH,
            available_time=now,
            fee=150,
            status=SkillPost.STATUS_PENDING,
        )

        self.client.login(username="student1", password="Pass12345!")

    def test_search_by_keyword_matches_title_or_description_or_provider(self):
        response = self.client.get(reverse("accounts:skills"), {"q": "python"})
        self.assertContains(response, "Python for Beginners")
        self.assertNotContains(response, "Figma UI Design")

        response = self.client.get(reverse("accounts:skills"), {"q": "wireframing"})
        self.assertContains(response, "Figma UI Design")

        response = self.client.get(reverse("accounts:skills"), {"q": "joy"})
        self.assertContains(response, "Python for Beginners")

    def test_filter_by_category_and_mode(self):
        response = self.client.get(reverse("accounts:skills"), {"category": SkillPost.CATEGORY_TECHNICAL})
        self.assertContains(response, "Python for Beginners")
        self.assertNotContains(response, "Figma UI Design")

        response = self.client.get(reverse("accounts:skills"), {"mode": SkillPost.MODE_OFFLINE})
        self.assertContains(response, "Figma UI Design")
        self.assertNotContains(response, "Python for Beginners")

    def test_only_approved_posts_are_shown(self):
        response = self.client.get(reverse("accounts:skills"))
        self.assertContains(response, "Python for Beginners")
        self.assertContains(response, "Figma UI Design")
        self.assertNotContains(response, "Hidden Pending Skill")

    def test_skill_detail_requires_approved_post(self):
        response = self.client.get(reverse("accounts:skill_detail", args=[self.python_post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python for Beginners")
