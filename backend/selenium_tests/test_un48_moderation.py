import unittest
from datetime import timedelta

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils import timezone
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from accounts.models import CustomUser, SkillPost


class SkillPostModerationSeleniumTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        try:
            cls.driver = webdriver.Chrome(options=chrome_options)
            cls.driver.set_window_size(1440, 900)
        except WebDriverException as exc:
            raise unittest.SkipTest(f"Chrome WebDriver is not available: {exc}")

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "driver"):
            try:
                cls.driver.quit()
            except Exception:
                pass
        super().tearDownClass()

    def setUp(self):
        self.wait = WebDriverWait(self.driver, 10)

        self.student = CustomUser.objects.create_user(
            username="student_un48",
            password="Pass12345!",
            email="23101084@uap-bd.edu",
            role="student",
        )
        self.admin = CustomUser.objects.create_user(
            username="admin_un48",
            password="AdminPass123!",
            email="admin@uap-bd.edu",
            role="alumni",
            is_staff=True,
            is_superuser=True,
        )

    def login(self, username, password):
        self.driver.get(f"{self.live_server_url}/login/")
        self.wait.until(EC.presence_of_element_located((By.ID, "id_username"))).send_keys(username)
        self.driver.find_element(By.ID, "id_password").send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    def create_pending_post(self, title="Moderation Test Skill"):
        return SkillPost.objects.create(
            provider=self.student,
            title=title,
            description="A test description for moderation.",
            category=SkillPost.CATEGORY_TECHNICAL,
            session_mode=SkillPost.MODE_ONLINE,
            available_time=timezone.now() + timedelta(days=2),
            fee=500,
            status=SkillPost.STATUS_PENDING,
        )

    def test_admin_can_approve_pending_post(self):
        post = self.create_pending_post(title="Approval Flow Skill")

        self.login("admin_un48", "AdminPass123!")
        self.driver.get(f"{self.live_server_url}/moderation/")

        review_link = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f"a[href='/moderation/{post.id}/']"))
        )
        review_link.click()

        approve_radio = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='action'][value='approve']"))
        )
        approve_radio.click()
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        self.wait.until(lambda _: SkillPost.objects.get(id=post.id).status == SkillPost.STATUS_APPROVED)

        post.refresh_from_db()
        self.assertEqual(post.status, SkillPost.STATUS_APPROVED)
        self.assertEqual(post.rejection_reason, "")

    def test_admin_reject_and_student_sees_reason(self):
        reason = "Please provide a clearer and more complete description."
        post = self.create_pending_post(title="Rejection Flow Skill")

        self.login("admin_un48", "AdminPass123!")
        self.driver.get(f"{self.live_server_url}/moderation/{post.id}/")

        reject_radio = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='action'][value='reject']"))
        )
        reject_radio.click()

        reason_box = self.driver.find_element(By.ID, "id_rejection_reason")
        reason_box.clear()
        reason_box.send_keys(reason)

        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        self.wait.until(lambda _: SkillPost.objects.get(id=post.id).status == SkillPost.STATUS_REJECTED)

        post.refresh_from_db()
        self.assertEqual(post.status, SkillPost.STATUS_REJECTED)
        self.assertEqual(post.rejection_reason, reason)

        self.driver.get(f"{self.live_server_url}/logout/")
        self.login("student_un48", "Pass12345!")
        self.driver.get(f"{self.live_server_url}/skills.html")

        # My Skill Posts table should show rejected status and reason for the owner.
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        page_source = self.driver.page_source

        self.assertIn("Rejection Flow Skill", page_source)
        self.assertIn("Rejected", page_source)
        self.assertIn(reason, page_source)
