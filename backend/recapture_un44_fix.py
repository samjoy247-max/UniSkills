from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
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

    # Go to dashboard to find user's posts
    driver.get('http://127.0.0.1:8000/dashboard.html')
    time.sleep(1)
    p = os.path.join(base_dir,'UN-44-A_my_posts_list_real.png')
    driver.save_screenshot(p)
    print('Saved:',p)

    # Try to find a link to the first skill detail page
    skill_links = driver.find_elements(By.XPATH, "//main//a[contains(@href,'/skill/')]")
    if not skill_links:
        skill_links = driver.find_elements(By.XPATH, "//main//h4/..//a[contains(@href,'/skill/')]")

    if skill_links:
        detail_href = skill_links[0].get_attribute('href')
        driver.get(detail_href)
        time.sleep(1)
        p = os.path.join(base_dir,'UN-44-1_skill_detail_real.png')
        driver.save_screenshot(p)
        print('Saved:',p)

        # Look for edit link/button on detail page
        try:
            edit = driver.find_element(By.XPATH,"//a[contains(@href,'/edit') or contains(@href,'edit') or contains(text(),'Edit')]")
            edit.click()
            time.sleep(1)
            p = os.path.join(base_dir,'UN-44-2_edit_skill_post_form_real.png')
            driver.save_screenshot(p)
            print('Saved:',p)

            # Submit without changes
            try:
                driver.find_element(By.CSS_SELECTOR,'button[type="submit"]').click()
                time.sleep(1)
                p = os.path.join(base_dir,'UN-44-2_edit_saved_real.png')
                driver.save_screenshot(p)
                print('Saved:',p)
            except Exception:
                pass
        except Exception as e:
            print('Edit link not found on detail page:',e)

        # Return to detail page and attempt delete
        driver.get(detail_href)
        time.sleep(1)
        try:
            delete = driver.find_element(By.XPATH,"//a[contains(@href,'/delete') or contains(text(),'Delete')]")
            delete.click()
            time.sleep(1)
            p = os.path.join(base_dir,'UN-44-3_delete_confirmation_real.png')
            driver.save_screenshot(p)
            print('Saved:',p)
        except Exception as e:
            print('Delete link not found on detail page:',e)
    else:
        print('No skill detail links found in dashboard')

finally:
    driver.quit()