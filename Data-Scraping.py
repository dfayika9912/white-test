import pandas as pd  
import requests  
from bs4 import BeautifulSoup  
from datetime import datetime, timedelta  
  
# Constants  
SWIFTBET_RACING_URL = "https://www.swiftbet.com.au/racing"  
  
def scrape_race_data(url):  
   """Scrape race data from SwiftBet"""  
   response = requests.get(url)  
   soup = BeautifulSoup(response.content, 'html.parser')  
  
   # Find all race cards  
   race_cards = soup.find_all('div', class_='race-card')  
  
   # Initialize lists to store scraped data  
   track_names = []  
   race_numbers = []  
   race_urls = []  
   race_times = []  
  
   # Scrape data from each race card  
   for race_card in race_cards:  
      track_name = race_card.find('span', class_='track-name').text.strip()  
      track_names.append(track_name)  
  
      race_number = race_card.find('span', class_='race-number').text.strip()  
      race_numbers.append(race_number)  
  
      race_url = SWIFTBET_RACING_URL + race_card.find('a', class_='race-link')['href']  
      race_urls.append(race_url)  
  
      time_to_race_start = race_card.find('span', class_='time-to-race-start').text.strip()  
      days, hours, minutes, seconds = map(int, time_to_race_start.split(':'))  
      delta = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)  
      now = datetime.now()  
      if delta.days == 0:  
        race_time = (now + delta).strftime('%Y-%m-%d %H:%M')  
      else:  
        race_time = (now + timedelta(days=1) + delta).strftime('%Y-%m-%d %H:%M')  
      race_times.append(race_time)  
  
   # Create a DataFrame and save it as a CSV file  
   df_races_data = pd.DataFrame({  
      'Track Name': track_names,  
      'Race Number': race_numbers,  
      'Race URL': race_urls,  
      'Race Time': race_times  
   })  
  
   df_races_data.to_csv('races_data.csv', index=False)  
   print("Data saved to races_data.csv")  
  
scrape_race_data(SWIFTBET_RACING_URL)
