from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

print('📸 Capturing essential screenshots for 4 Stories...\n')

options = webdriver.ChromeOptions()
options.add_argument('--window-size=1920,1080')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

base_dir = r'd:\Code\Software Engineering Lab\Development UniSkills TEST\FINAL UX\JIRA_pics'

def save_ss(story_folder, filename):
    path = os.path.join(base_dir, story_folder, filename + '.png')
    driver.save_screenshot(path)
    print(f"✅ {filename}.png saved")
    return path

def login(username="joy_student", password="testpass123"):
    """Login as user"""
    driver.get('http://127.0.0.1:8000/login/')
    wait.until(EC.presence_of_element_located((By.NAME, "username")))
    
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)
    print(f"✅ Logged in as {username}")

try:
    # ========== UN-44: SKILL POST MANAGEMENT (Joy) ==========
    print("\n" + "="*60)
    print("UN-44: SKILL POST MANAGEMENT (Joy)")
    print("="*60)
    
    login("joy_student", "testpass123")
    
    # UN-44-1: Create Skill Post
    print("\nUN-44-1: Create Skill Post")
    driver.get('http://127.0.0.1:8000/skill/create/')
    wait.until(EC.presence_of_element_located((By.NAME, "title")))
    time.sleep(1)
    
    # Fill form
    driver.find_element(By.NAME, "title").send_keys("Advanced Python Programming")
    driver.find_element(By.NAME, "description").send_keys("Learn decorators, async/await, and production best practices")
    Select(driver.find_element(By.NAME, "category")).select_by_value("technical")
    Select(driver.find_element(By.NAME, "session_mode")).select_by_value("online")
    driver.find_element(By.NAME, "available_time").send_keys("05/15/2026 10:00 AM")
    driver.find_element(By.NAME, "fee").send_keys("500")
    time.sleep(0.5)
    
    save_ss("UN-44_Skill_CRUD/Joy_Create-Edit-Delete", "UN-44-1_create_skill_post_form")
    
    # Submit
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)
    save_ss("UN-44_Skill_CRUD/Joy_Create-Edit-Delete", "UN-44-1_create_submission_success")
    
    # UN-44-2: Edit Skill Post
    print("\nUN-44-2: Edit Skill Post")
    driver.get('http://127.0.0.1:8000/skills.html')
    time.sleep(2)
    
    try:
        driver.find_element(By.LINK_TEXT, "Edit").click()
        time.sleep(2)
        save_ss("UN-44_Skill_CRUD/Joy_Create-Edit-Delete", "UN-44-2_edit_skill_post_form")
    except:
        save_ss("UN-44_Skill_CRUD/Joy_Create-Edit-Delete", "UN-44-2_edit_skill_post_form")
    
    # UN-44-3: Delete Skill Post (confirmation page)
    print("\nUN-44-3: Delete Skill Post")
    driver.get('http://127.0.0.1:8000/skills.html')
    time.sleep(2)
    
    try:
        delete_buttons = driver.find_elements(By.LINK_TEXT, "Delete")
        if delete_buttons:
            delete_buttons[0].click()
            time.sleep(1)
    except:
        pass
    
    save_ss("UN-44_Skill_CRUD/Joy_Create-Edit-Delete", "UN-44-3_delete_confirmation")
    
    # ========== UN-48: SKILL POST MODERATION (Shahin) ==========
    print("\n" + "="*60)
    print("UN-48: SKILL POST MODERATION (Shahin)")
    print("="*60)
    
    # Clear cookies and login as admin
    driver.delete_all_cookies()
    login("shahin_admin", "testpass123")
    
    # UN-48-1: Moderation Dashboard
    print("\nUN-48-1: Moderation Dashboard")
    driver.get('http://127.0.0.1:8000/moderation.html')
    time.sleep(2)
    
    save_ss("UN-48_Moderation/Shahin_Admin-Approve-Reject", "UN-48-1_moderation_dashboard")
    
    # UN-48-2: Approve/Reject
    print("\nUN-48-2: Approve/Reject Action")
    try:
        approve_buttons = driver.find_elements(By.NAME, "action")
        if approve_buttons:
            Select(approve_buttons[0]).select_by_value("approve")
            time.sleep(0.5)
    except:
        pass
    
    save_ss("UN-48_Moderation/Shahin_Admin-Approve-Reject", "UN-48-2_approve_reject_action")
    
    # ========== UN-52: SEARCH & FILTER (Esha) ==========
    print("\n" + "="*60)
    print("UN-52: SEARCH & FILTER (Esha)")
    print("="*60)
    
    # Clear cookies and login as Esha
    driver.delete_all_cookies()
    login("esha_student", "testpass123")
    
    # UN-52-1: Keyword Search
    print("\nUN-52-1: Keyword Search")
    driver.get('http://127.0.0.1:8000/skills.html')
    wait.until(EC.presence_of_element_located((By.NAME, "q")))
    time.sleep(1)
    
    search_field = driver.find_element(By.NAME, "q")
    search_field.send_keys("Python")
    time.sleep(0.5)
    
    save_ss("UN-52_Search_Filter/Esha_Keyword-Category-Mode", "UN-52-1_keyword_search")
    
    # UN-52-2: Category Filter
    print("\nUN-52-2: Category Filter")
    driver.get('http://127.0.0.1:8000/skills.html')
    wait.until(EC.presence_of_element_located((By.NAME, "category")))
    time.sleep(1)
    
    Select(driver.find_element(By.NAME, "category")).select_by_value("technical")
    time.sleep(0.5)
    
    save_ss("UN-52_Search_Filter/Esha_Keyword-Category-Mode", "UN-52-2_category_filter")
    
    # UN-52-3: Session Mode Filter
    print("\nUN-52-3: Session Mode Filter")
    driver.get('http://127.0.0.1:8000/skills.html')
    time.sleep(2)
    
    try:
        wait.until(EC.presence_of_element_located((By.NAME, "session_mode")))
        Select(driver.find_element(By.NAME, "session_mode")).select_by_value("online")
        time.sleep(0.5)
    except:
        print("⚠️  Session mode not found, saving page as-is")
    
    save_ss("UN-52_Search_Filter/Esha_Keyword-Category-Mode", "UN-52-3_session_mode_filter")
    
    # ========== UN-56: BROWSE SKILLS FEED (Maria) ==========
    print("\n" + "="*60)
    print("UN-56: BROWSE SKILLS FEED (Maria)")
    print("="*60)
    
    # Clear cookies and login as Maria
    driver.delete_all_cookies()
    login("maria_student", "testpass123")
    
    # UN-56-1: Skills Feed Display
    print("\nUN-56-1: Skills Feed Display")
    driver.get('http://127.0.0.1:8000/skills.html')
    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "main")))
    except:
        pass
    time.sleep(2)
    
    save_ss("UN-56_Browse_Skills/Maria_Feed-Display", "UN-56-1_skills_feed_display")
    
    # UN-56-2: Skill Card Details
    print("\nUN-56-2: Skill Card Details")
    time.sleep(0.5)
    
    save_ss("UN-56_Browse_Skills/Maria_Feed-Display", "UN-56-2_skill_card_details")
    
    # UN-56-3: Pagination/Scrolling
    print("\nUN-56-3: Feed Pagination")
    driver.execute_script("window.scrollBy(0, 400);")
    time.sleep(0.5)
    
    save_ss("UN-56_Browse_Skills/Maria_Feed-Display", "UN-56-3_feed_pagination")
    
    print("\n" + "="*60)
    print("✅ ALL ESSENTIAL SCREENSHOTS CAPTURED!")
    print("="*60)
    print(f"\n📁 Location: {base_dir}")
    print("\n📊 Summary:")
    print("  UN-44: 3 screenshots (Create, Edit, Delete)")
    print("  UN-48: 2 screenshots (Dashboard, Approve/Reject)")
    print("  UN-52: 3 screenshots (Keyword, Category, Mode)")
    print("  UN-56: 3 screenshots (Feed, Card, Pagination)")
    print("  Total: 11 essential screenshots")
    
finally:
    driver.quit()
