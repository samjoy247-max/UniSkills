from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

base_dir = r'd:\Code\Software Engineering Lab\Development UniSkills TEST\FINAL UX\JIRA_pics\UN-48_Moderation\Shahin_Admin-Approve-Reject'
options = webdriver.ChromeOptions()
options.add_argument('--window-size=1920,1080')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

try:
    # login as admin
    driver.get('http://127.0.0.1:8000/login/')
    wait.until(EC.presence_of_element_located((By.NAME,'username')))
    driver.find_element(By.NAME,'username').send_keys('shahin_admin')
    driver.find_element(By.NAME,'password').send_keys('testpass123')
    driver.find_element(By.CSS_SELECTOR,'button[type="submit"]').click()
    time.sleep(2)

    # Go to moderation page
    driver.get('http://127.0.0.1:8000/moderation.html')
    time.sleep(2)
    p = os.path.join(base_dir,'UN-48-1_moderation_dashboard_real.png')
    driver.save_screenshot(p)
    print('Saved:',p)

    # Try to find first pending post and capture approve UI
    try:
        pending = driver.find_element(By.XPATH, "//tr[.//td[contains(text(),'Pending')]]")
        p2 = os.path.join(base_dir,'UN-48-2_pending_row.png')
        driver.save_screenshot(p2)
        print('Saved:',p2)
    except Exception as e:
        print('Could not find pending row:',e)

finally:
    driver.quit()