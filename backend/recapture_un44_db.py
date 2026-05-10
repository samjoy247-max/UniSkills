import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','uniskills_backend.settings')
django.setup()
from accounts.models import CustomUser, SkillPost

# find first demo skill for joy_student
user = CustomUser.objects.filter(username='joy_student').first()
if not user:
    raise SystemExit('joy_student not found')

skill = SkillPost.objects.filter(provider=user).order_by('id').first()
if not skill:
    raise SystemExit('No SkillPost found for joy_student')

skill_id = skill.id
print('Found skill id:', skill_id)

# now run selenium capture using that id
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

base_dir = r'd:\Code\Software Engineering Lab\Development UniSkills TEST\FINAL UX\JIRA_pics\UN-44_Skill_CRUD\Joy_Create-Edit-Delete'
options = webdriver.ChromeOptions()
options.add_argument('--window-size=1920,1080')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

try:
    # login
    driver.get('http://127.0.0.1:8000/login/')
    wait.until(EC.presence_of_element_located((By.NAME,'username')))
    driver.find_element(By.NAME,'username').send_keys('joy_student')
    driver.find_element(By.NAME,'password').send_keys('testpass123')
    driver.find_element(By.CSS_SELECTOR,'button[type="submit"]').click()
    time.sleep(2)

    detail_url = f'http://127.0.0.1:8000/skill/{skill_id}/'
    driver.get(detail_url)
    time.sleep(1)
    p = os.path.join(base_dir,f'UN-44_detail_{skill_id}.png')
    driver.save_screenshot(p)
    print('Saved:',p)

    # edit link: try to navigate to edit URL
    edit_url = f'http://127.0.0.1:8000/skill/{skill_id}/edit/'
    driver.get(edit_url)
    time.sleep(1)
    p = os.path.join(base_dir,f'UN-44_edit_form_{skill_id}.png')
    driver.save_screenshot(p)
    print('Saved:',p)

    # submit edit without change
    try:
        driver.find_element(By.CSS_SELECTOR,'button[type="submit"]').click()
        time.sleep(1)
        p = os.path.join(base_dir,f'UN-44_edit_saved_{skill_id}.png')
        driver.save_screenshot(p)
        print('Saved:',p)
    except Exception as e:
        print('Could not submit edit form:',e)

    # delete URL
    delete_url = f'http://127.0.0.1:8000/skill/{skill_id}/delete/'
    driver.get(delete_url)
    time.sleep(1)
    p = os.path.join(base_dir,f'UN-44_delete_confirm_{skill_id}.png')
    driver.save_screenshot(p)
    print('Saved:',p)

finally:
    driver.quit()