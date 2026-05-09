from datetime import timedelta

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils import timezone
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from accounts.models import CustomUser, SkillPost


class UN44SkillPostFlowSeleniumTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1366,900")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.set_page_load_timeout(25)
        cls.wait = WebDriverWait(cls.driver, 15)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        self.password = "TestPass123!"
        self.student = CustomUser.objects.create_user(
            username="sj_selenium",
            email="sj_selenium@uap-bd.edu",
            password=self.password,
            role="student",
            is_active=True,
        )

    def _login(self):
        self.driver.get(f"{self.live_server_url}/login/")
        self.wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(self.student.username)
        self.driver.find_element(By.NAME, "password").send_keys(self.password)
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        self.wait.until(EC.url_contains("dashboard"))

    def test_student_can_create_skill_post_with_pending_status(self):
        self._login()

        self.driver.get(f"{self.live_server_url}/skills.html")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        body_text = self.driver.find_element(By.TAG_NAME, "body").text
        self.assertIn("Browse Skills", body_text, msg=f"Unexpected page at {self.driver.current_url}")
        self.assertIn(
            "My Skill Posts",
            body_text,
            msg=f"Student create/manage section missing at {self.driver.current_url}.",
        )

        title_field = self.wait.until(EC.presence_of_element_located((By.ID, "id_title")))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", title_field)
        slot = (timezone.now() + timedelta(days=2)).strftime("%Y-%m-%dT%H:%M")
        self.driver.execute_script(
            """
            document.getElementById('id_title').value = arguments[0];
            document.getElementById('id_description').value = arguments[1];
            document.getElementById('id_category').value = arguments[2];
            document.getElementById('id_session_mode').value = arguments[3];
            document.getElementById('id_available_time').value = arguments[4];
            document.getElementById('id_fee').value = arguments[5];
            """,
            "Selenium Skill Post",
            "Automated E2E test description for UN-44",
            "technical",
            "online",
            slot,
            "250",
        )
        create_form = self.driver.find_element(By.XPATH, "//form[.//input[@name='title']]")
        self.driver.execute_script("arguments[0].submit();", create_form)

        self.wait.until(
            lambda _driver: SkillPost.objects.filter(
                title="Selenium Skill Post",
                provider=self.student,
            ).exists()
        )

        created_post = SkillPost.objects.get(title="Selenium Skill Post", provider=self.student)
        self.assertEqual(created_post.status, SkillPost.STATUS_PENDING)
        self.assertTrue(
            self.driver.find_elements(By.CSS_SELECTOR, f"a[href*='edit={created_post.id}']"),
            msg="Created post should appear in My Skill Posts with Edit action.",
        )
