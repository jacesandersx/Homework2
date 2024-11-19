#BusSchedule.py
#Name: Jace Sanders 
#Date: 10/24/2024
#Assignment: Bus Schedule


#Some of these functions aren't used in the def main() but didn't want to delete them so you could still see. Thanks

from bs4 import  BeautifulSoup

from datetime import datetime, timezone, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def loadURL(url):
  """
  This function loads a given URL and returns the text
  that is displayed on the site. It does not return the
  raw HTML code but only the code that is visible on the page.
  """
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  chrome_options.add_argument("--headless");
  driver = webdriver.Chrome(options=chrome_options)
  driver.get(url)
  content=driver.find_element(By.XPATH, "/html/body").text
  driver.quit()

  return content

def loadTestPage():
  """
  This function returns the contents of our test page.
  This is done to avoid unnecessary calls to the site
  for our testing.
  """
  page = open("testPage.txt", 'r')
  contents = page.read()
  page.close()

  return contents

def isLater(time1, time2):

  return time1 > time2

def getHours(time):
  parts = time.split()
  hoursMin = parts[0].split(':')
  period = parts[1]

  hour = int(hoursMin[0])
  if period == 'PM' and hour != 12:
    hour += 12
  elif period == 'AM' and hour == 12:
    hour = 0
  return hour

def getMin(time):
  minutes = int(time.split()[0].split(':')[1])
  return minutes

def getTime(): 
  now = datetime.now() - timedelta(hours=5)
  hour = now.hour
  minute = now.minute
    
  period = "AM" if hour < 12 else "PM"
  if hour > 12:
        hour -= 12
  elif hour == 0:
        hour = 12 

  regTime = f"{hour}:{minute:02d} {period}"
  return regTime

def timeDif(scheduledTime):
  currentTime = datetime.now()
  timeDiff = scheduledTime - currentTime
  return timeDiff.total_seconds() // 60

def extractBusTimes(html_content):
    """Extract bus times from HTML and return as a list of formatted datetime objects."""
    soup = BeautifulSoup(html_content, 'html.parser')

    
    bus_times = []
    for time_tag in soup.find_all('li'):  
        time_text = time_tag.get_text(strip=True)
        bus_times.append(time_text)
    return bus_times

def convert_to_datetime(time_str):
    """Convert a time string 'HH:MM AM/PM' to a datetime object for today."""
    hour = getHours(time_str)
    minute = getMin(time_str)
    now = datetime.now()
    return now.replace(hour=hour, minute=minute, second=0, microsecond=0)

def main():
  url = "https://myride.ometro.com/Schedule?stopCode=1264&date=2024-10-24&routeNumber=24&directionName=NORTH"
  #c1 = loadURL(url) #loads the web page
  c1 = loadTestPage() #loads the test page
  #print(c1)

  bus_times = extractBusTimes(c1)

  currentTime = getTime()

  print(f"Current Time: {currentTime}")

  next_bus_time = None
  for bus_time in bus_times:
      scheduled_time = convert_to_datetime(bus_time)
      if scheduled_time > datetime.now():  
          next_bus_time = scheduled_time
          break 
    
  if next_bus_time:        
    minutes_to_bus = timeDif(next_bus_time)
    print(f"The next bus will arrive in {int(minutes_to_bus)} minutes")
    print(f"The following bus will arrive in {int(minutes_to_bus)} minutes")
  else:
     print("No upcoming busses.")
  
  #scheduledTime = datetime.now() 
  #minutes_to_bus = timeDif(scheduledTime)

  #print("The next bus will arrive in:", minutes_to_bus ,"minutes")
  #print("The following bus will arrive in:", minutes_to_bus + 30 , "minutes")
  
  

main()
