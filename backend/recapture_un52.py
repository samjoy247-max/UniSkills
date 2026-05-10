from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

base_dir = r'd:\Code\Software Engineering Lab\Development UniSkills TEST\FINAL UX\JIRA_pics\UN-52_Search_Filter\Esha_Keyword-Category-Mode'
options = webdriver.ChromeOptions()
options.add_argument('--window-size=1920,1080')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

try:
    # login as esha
    driver.get('http://127.0.0.1:8000/login/')
    wait.until(EC.presence_of_element_located((By.NAME,'username')))
    driver.find_element(By.NAME,'username').send_keys('esha_student')
    driver.find_element(By.NAME,'password').send_keys('testpass123')
    driver.find_element(By.CSS_SELECTOR,'button[type="submit"]').click()
    time.sleep(2)

    # Keyword search
    driver.get('http://127.0.0.1:8000/skills.html')
    wait.until(EC.presence_of_element_located((By.NAME,'q')))
    q = driver.find_element(By.NAME,'q')
    q.clear()
    q.send_keys('UniSkillsDemoSearch')
    q.submit()
    time.sleep(2)
    p = os.path.join(base_dir,'UN-52-1_keyword_search_real.png')
    driver.save_screenshot(p)
    print('Saved:',p)

    # Category filter
    driver.get('http://127.0.0.1:8000/skills.html')
    wait.until(EC.presence_of_element_located((By.NAME,'category')))
    Select(driver.find_element(By.NAME,'category')).select_by_value('technical')
    time.sleep(1)
    p = os.path.join(base_dir,'UN-52-2_category_filter_real.png')
    driver.save_screenshot(p)
    print('Saved:',p)

    # Session mode filter
    driver.get('http://127.0.0.1:8000/skills.html')
    try:
        wait.until(EC.presence_of_element_located((By.NAME,'session_mode')))
        Select(driver.find_element(By.NAME,'session_mode')).select_by_value('online')
    except:
        pass
    time.sleep(1)
    p = os.path.join(base_dir,'UN-52-3_session_mode_filter_real.png')
    driver.save_screenshot(p)
    print('Saved:',p)

finally:
    driver.quit()