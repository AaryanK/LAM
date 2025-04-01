from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service  # For Edge, the same import is used
from selenium.webdriver.common.keys import Keys
from webdriver_manager.microsoft import EdgeDriverManager  # Specific manager for Edge
import time

# Set up Edge options
edge_options = webdriver.EdgeOptions('msedgedriver.exe')
edge_options.add_argument('--headless')  # Optional: Run in headless mode

# Initialize WebDriver for Microsoft Edge
driver = webdriver.Edge(service=Service(EdgeDriverManager().install()), options=edge_options)

# Open the website you want to scrape
driver.get('https://example.com')  # Replace with your target URL

# Wait for the page to load
time.sleep(3)

# Scrape the data
# Example: Extracting all paragraph texts on the page
paragraphs = driver.find_elements(By.TAG_NAME, 'p')  # Extract all <p> tags

# Print the content of the paragraphs
for para in paragraphs:
    print(para.text)

# Close the browser once scraping is done
driver.quit()
