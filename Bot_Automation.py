import pandas as pd  
from selenium import webdriver  
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  
from selenium.common.exceptions import TimeoutException  
  
# Constants  
SWIFTBET_RACING_URL = "https://www.swiftbet.com.au/racing"  
  
def automate_bot():  
   # Load race data and select a random race  
   df_races_data = pd.read_csv('races_data.csv')  
   random_race = df_races_data.sample(n=1).iloc[0]  
   track_name = random_race['Track Name']  
   race_number = random_race['Race Number']  
  
   # Set up Selenium WebDriver  
   options = webdriver.ChromeOptions()  
   options.add_argument('headless')  # Run in headless mode (optional)  
   driver = webdriver.Chrome(options=options)  
  
   try:  
      # Navigate to the main races selection page  
      driver.get(SWIFTBET_RACING_URL)  
  
      # Find and click on the track selection element  
      track_selector = WebDriverWait(driver, 10).until(  
        EC.presence_of_element_located((By.XPATH, f"//div[text()='{track_name}']"))  
      )  
      track_selector.click()  
  
      # Find and click on the race number selection element  
      race_number_selector = WebDriverWait(driver, 10).until(  
        EC.presence_of_element_located((By.XPATH, f"//div[text()='Race {race_number}']"))  
      )  
      race_number_selector.click()  
  
      # Scrape current market prices for horses participating in the selected race  
      horse_names = driver.find_elements(By.CLASS_NAME, 'horse-name')  
      market_prices = driver.find_elements(By.CLASS_NAME, 'market-price')  
  
      # Create a DataFrame and save it as a CSV file  
      df_performed_bets = pd.DataFrame({  
        'Horse Name': [horse.text.strip() for horse in horse_names],  
        'Market Price': [price.text.strip() for price in market_prices]  
      })  
  
      df_performed_bets.to_csv('performed_bets.csv', index=False)  
      print("Data saved to performed_bets.csv")  
  
   except TimeoutException:  
      print("Timed out waiting for page to load")  
   finally:  
      driver.quit()  
  
automate_bot()
