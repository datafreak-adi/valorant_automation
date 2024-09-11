from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

s = Service("C:/Users/ADITYA/OneDrive/Desktop/chromedriver.exe")

# set different options for the browser
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

# to remove errors
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--ignore-ssl-errors")

#maximize the browser
chrome_options.add_argument("start-maximized")

driver = webdriver.Chrome(service=s, options=chrome_options)

#site opening
driver.get("https://www.vlr.gg/event/matches/1015/valorant-champions-2022/?series_id=2184")
time.sleep(1)



# Function to extract elements, scroll, and save HTML content
def extract_elements_html_with_navigation_to_file(n_start, n_end):
    for n in range(n_start, n_end + 1, 2):  # Iterate over the changing div numbers
        for a_index in range(1, 3):  # Assuming you're alternating between 'a[1]' and 'a[2]'
            xpath = f'//*[@id="wrapper"]/div[1]/div/div[{n}]/a[{a_index}]'
            if n==16 or n==18:
              xpath = f'//*[@id="wrapper"]/div[1]/div/div[{n}]/a]'
              a_index=3

            try:
                # Click the link to navigate to the new page
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(3)  # Wait for the new page to load

                # Wait for the target content section to be present
                target_xpath = '//*[@id="wrapper"]/div[1]/div[3]/div[6]/div/div[3]'
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, target_xpath)))

                # Find the scrollable section
                scrollable_element = driver.find_element(By.XPATH, target_xpath)
                last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_element)

                # Scroll within the specific section
                while True:
                    # Scroll down within the specific section
                    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_element)

                    # Wait for the content to load
                    time.sleep(2)

                    # Calculate new scroll height and compare with the last scroll height
                    new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_element)

                    if new_height == last_height:
                        break  # Exit the loop if no new content is loaded

                    last_height = new_height

                # After scrolling, get the HTML content of the specific section
                specific_section_html = scrollable_element.get_attribute('outerHTML')

                # Save the specific HTML content to a file
                filename = f"page_{n}_a{a_index}.html"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(specific_section_html)

                # Navigate back to the previous page
                driver.back()
                time.sleep(8)  # Wait for the previous page to load

            except Exception as e:
                print(f"Element not found for {xpath}: {str(e)}")

    # Optional sleep between iterations
time.sleep(1)


# Call the function to extract and save HTML content
extract_elements_html_with_navigation_to_file(4, 14)

#close the chrome browser
driver.quit()