import webview
import time
import win32gui
import win32con
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Read password.txt file
with open("password.txt", "r") as file:
    lines = file.readlines()
    USERNAME = lines[0].strip()
    PASSWORD = lines[1].strip()

options = Options()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)

wait = WebDriverWait(driver, 10)


# Login
try:
    driver.get("https://elearning.tdtu.edu.vn/login/index.php")
    driver.find_element(By.ID, "username").send_keys(USERNAME)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.ID, "loginbtn").click()
    wait.until(
        EC.url_contains("https://elearning.tdtu.edu.vn/course/index.php")
    )
except Exception as e:
    print(f"Error during login: {e}")
    driver.quit()
    exit(1)

# Access the dashboard page
try:
    driver.get("https://elearning.tdtu.edu.vn/my/")
    #Wait to have the timeline block loaded
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "section.block_timeline #page-container-3 .event-name-container"))
    )
    timeline_element = driver.find_element(By.CSS_SELECTOR, "section.block_timeline")

    timeline = timeline_element.get_attribute("outerHTML")
except Exception as e:
    print(f"Error accessing dashboard: {e}")
    driver.quit()
    exit(1)

driver.quit()

# Create the HTML and CSS for the webview
html = f"""
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            background-color: #f8f9fa;
            font-family: "Segoe UI", Roboto, sans-serif;
            margin: 0;
            padding: 20px;
        }}
        /* General styles for the block */
        /* Hide the header of the block to simplify the UI */
        #instance-414758-header {{
            display: none;
        }}
        /* Ensure the timeline block is visible */
        .block_timeline {{
            display: block;
        }}

        /* Hide the dropdown menu for time filters */
        .block_timeline [data-region="day-filter"] .dropdown-menu {{
            display: none !important;
        }}

        /* Hide the sort selector dropdown */
        .block_timeline [data-region="view-selector"] .dropdown-menu {{
            display: none !important;
        }}

        /* Hide the sort selector button text and icon to simplify the UI */
        .block_timeline [data-region="view-selector"] .btn {{
            display: none;
        }}

        /* Hide the paging control (Show 5, 10, 25 options and navigation) */
        .block_timeline [data-region="paging-control-container"] {{
            display: none !important;
        }}

        /* Hide the courses view tab */
        .block_timeline [data-region="view-courses"] {{
            display: none !important;
        }}

        /* Hide the empty message section */
        .block_timeline [data-region="empty-message"] {{
            display: none !important;
        }}

        /* Hide the loading placeholder */
        .block_timeline [data-region="event-list-loading-placeholder"] {{
            display: none !important;
        }}

        /* Hide the course items loading placeholder */
        .block_timeline [data-region="course-items-loading-placeholder"] {{
            display: none !important;
        }}

        /* Style the event list container for better presentation */
        .block_timeline [data-region="event-list-container"] {{
            margin-top: 10px;
        }}

        /* Style the event list items */
        .block_timeline .list-group-item[data-region="event-list-item"] {{
            padding: 10px 0;
            border-bottom: 1px solid #e0e0e0;
        }}

        /* Style the event name and course title */
        .block_timeline .event-name-container h6.event-name {{
            font-size: 16px;
            font-weight: bold;
            margin: 0;
        }}

        .block_timeline .event-name-container small.text-muted {{
            font-size: 12px;
            color: #666;
        }}

        /* Style the action link (e.g., "Add submission") */
        .block_timeline .event-name-container a.list-group-item-action {{
            font-size: 14px;
            color: #007bff;
            text-decoration: none;
        }}

        .block_timeline .event-name-container a.list-group-item-action:hover {{
            text-decoration: underline;
        }}

        /* Style the timestamp */
        .block_timeline small.text-right {{
            font-size: 12px;
            color: #333;
        }}

        /* Hide the filter button text to simplify the UI */
        .block_timeline [data-region="day-filter"] .btn .sr-only {{
            display: none;
        }}

        /* Style the filter button to show only the clock icon */
        .block_timeline [data-region="day-filter"] .btn {{
            padding: 5px;
            border: none;
            background: transparent;
        }}

        /* Style the date header */
        .block_timeline .h6.mt-3 {{
            font-size: 14px;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }}
    </style>
</head>
<body>
    {timeline}
</body>
</html>
"""

# Set window position
def set_window_pos():
    time.sleep(1)
    hwnd = win32gui.FindWindow(None, "📅 Upcoming deadlines")
    if hwnd:
        screen_width = win32gui.GetSystemMetrics(0)
        screen_height = win32gui.GetSystemMetrics(1)
        x = screen_width - 350 - 10
        y = 10
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, x, y, 350, 600, 0)

window = webview.create_window("📅 Upcoming deadlines", html=html, width=350, height=600, resizable=True, on_top=True)
threading.Thread(target=set_window_pos, daemon=True).start()
webview.start()