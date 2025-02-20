import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv

# Set up logging to file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log', mode='w', encoding='utf-8'),
        logging.StreamHandler()  # Also log to the console
    ]
)
logger = logging.getLogger()

# Initialize the WebDriver
driver = webdriver.Chrome()

try:
    # Open the login page
    logger.info("Opening the login page.")
    driver.get("https://nuu-conference-admin.netlify.app/")
    time.sleep(3)  # Wait for the page to load
    
    # Input credentials and log in
    logger.info("Inputting login credentials.")
    driver.find_element(By.NAME, 'username').send_keys('johndoe')  # Corrected name attribute
    driver.find_element(By.NAME, 'password').send_keys('password')  # Corrected name attribute
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    time.sleep(5)  # Wait for the login to complete

    # Navigate to the table page
    logger.info("Navigating to the articles table page.")
    driver.get("https://nuu-conference-admin.netlify.app/#/article")
    time.sleep(5)  # Wait for the table to load

    # Open CSV file to write data
    logger.info("Opening CSV file to write articles data.")
    with open('csv\\articles_data.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # Extract headers
        table = driver.find_element(By.CLASS_NAME, 'MuiTable-root')
        headers = [header.text.strip() for header in table.find_elements(By.TAG_NAME, 'th')[1:7]]  # Skip the first column and take until the 7th
        writer.writerow(headers)
        logger.info(f"Extracted headers: {headers}")

        # Initialize row count
        row_count = 0
        
        while True:
            # Extract table data from current page
            rows = []
            logger.info("Extracting table data from current page.")
            for row in table.find_elements(By.TAG_NAME, 'tr'):
                cells = row.find_elements(By.TAG_NAME, 'td')
                if cells:
                    # Skip the first column, and handle links in the cells
                    row_data = []
                    for index, cell in enumerate(cells[1:7]):  # Skip first column and take until the 7th column
                        link = cell.find_elements(By.TAG_NAME, 'a')  # Find all <a> tags (links)
                        if link:  # If a link exists in this cell
                            href = link[0].get_attribute('href')  # Get the href attribute
                            row_data.append(href)  # Append the href to the row
                        else:
                            row_data.append(cell.text.strip()) 
                    rows.append(row_data)
            
            # Write rows to CSV and update row count
            writer.writerows(rows)
            row_count += len(rows)
            logger.info(f"Added {len(rows)} rows to CSV.")

            # Check if there is a "Next" page button and click it
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Go to next page"]')
                if "disabled" in next_button.get_attribute('class'):
                    logger.info("No more pages to load, stopping.")
                    break  # If the "Next" button is disabled, stop the loop
                next_button.click()  # Click the "Next" button
                time.sleep(5)  # Wait for the next page to load
            except Exception as e:
                logger.error(f"Error while trying to click the 'Next' button: {e}")
                break  # If no next button is found, stop the loop

    logger.info(f"Table data saved to 'csv\\articles_data.csv'. Total rows added: {row_count}")

    logger.info("Navigating to the use table page.")
    driver.get("https://nuu-conference-admin.netlify.app/#/user")
    time.sleep(5)  # Wait for the table to load

    # Open CSV file to write data
    logger.info("Opening CSV file to write users data.")
    with open('csv\\users_data.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # Extract headers
        table = driver.find_element(By.CLASS_NAME, 'MuiTable-root')
        headers = [header.text.strip() for header in table.find_elements(By.TAG_NAME, 'th')[1:7]]  # Skip the first column and take until the 7th
        writer.writerow(headers)
        logger.info(f"Extracted headers: {headers}")

        # Initialize row count
        row_count = 0
        
        while True:
            # Extract table data from current page
            rows = []
            logger.info("Extracting table data from current page.")
            for row in table.find_elements(By.TAG_NAME, 'tr'):
                cells = row.find_elements(By.TAG_NAME, 'td')
                if cells:
                    # Skip the first column, and handle links in the cells
                    row_data = []
                    for index, cell in enumerate(cells[1:7]):  # Skip first column and take until the 7th column
                        link = cell.find_elements(By.TAG_NAME, 'a')  # Find all <a> tags (links)
                        if link:  # If a link exists in this cell
                            href = link[0].get_attribute('href')  # Get the href attribute
                            row_data.append(href)  # Append the href to the row
                        else:
                            row_data.append(cell.text.strip()) 
                    rows.append(row_data)
            
            # Write rows to CSV and update row count
            writer.writerows(rows)
            row_count += len(rows)
            logger.info(f"Added {len(rows)} rows to CSV.")

            # Check if there is a "Next" page button and click it
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Go to next page"]')
                if "disabled" in next_button.get_attribute('class'):
                    logger.info("No more pages to load, stopping.")
                    break  # If the "Next" button is disabled, stop the loop
                next_button.click()  # Click the "Next" button
                time.sleep(5)  # Wait for the next page to load
            except Exception as e:
                logger.error(f"Error while trying to click the 'Next' button: {e}")
                break  # If no next button is found, stop the loop
    
    logger.info(f"Table data saved to 'csv\\users_data.csv'. Total rows added: {row_count}")
finally:
    driver.quit()
