from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

base_dir = r'd:\Code\Software Engineering Lab\Development UniSkills TEST\FINAL UX\JIRA_pics\UN-44_Skill_CRUD\Joy_Create-Edit-Delete'
options = webdriver.ChromeOptions()
options.add_argument('--window-size=1920,1080')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

try:
    # Login as joy_student
    driver.get('http://127.0.0.1:8000/login/')
    wait.until(EC.presence_of_element_located((By.NAME,'username')))
    driver.find_element(By.NAME,'username').send_keys('joy_student')
    driver.find_element(By.NAME,'password').send_keys('testpass123')
    driver.find_element(By.CSS_SELECTOR,'button[type="submit"]').click()
    time.sleep(2)

    # Go to dashboard or my posts page - try /dashboard.html then /my-posts if exists
    driver.get('http://127.0.0.1:8000/dashboard.html')
    time.sleep(1)
    # Save screenshot showing list of user's posts
    p = os.path.join(base_dir,'UN-44-A_my_posts_list.png')
    driver.save_screenshot(p)
    print('Saved:',p)

    # Click first Edit link for the created demo skill
    try:
        edit = driver.find_element(By.LINK_TEXT,'Edit')
        edit.click()
        time.sleep(1)
        p = os.path.join(base_dir,'UN-44-2_edit_skill_post_form_real.png')
        driver.save_screenshot(p)
        print('Saved:',p)

        # Change title and save
        title = driver.find_element(By.NAME,'title')
        title.clear()
        title.send_keys('Demo Skill 1 - Edited')
        driver.find_element(By.CSS_SELECTOR,'button[type="submit"]').click()
        time.sleep(1)
        p = os.path.join(base_dir,'UN-44-2_edit_saved_real.png')
        driver.save_screenshot(p)
        print('Saved:',p)
    except Exception as e:
        print('Edit not found or failed:',e)

    # Now delete the same post from dashboard
    driver.get('http://127.0.0.1:8000/dashboard.html')
    time.sleep(1)
    try:
        delete = driver.find_element(By.LINK_TEXT,'Delete')
        delete.click()
        time.sleep(1)
        p = os.path.join(base_dir,'UN-44-3_delete_confirmation_real.png')
        driver.save_screenshot(p)
        print('Saved:',p)
    except Exception as e:
        print('Delete not found or failed:',e)

finally:
    driver.quit()