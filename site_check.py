import requests
from bs4 import BeautifulSoup

def scrape_ingv_earthquakes():
    url = "https://terremoti.ingv.it"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code != 200:
        print("Failed to retrieve the webpage.")
        return
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract earthquake data (assuming table structure)
    earthquakes = []
    table = soup.find("table")  # Adjust this selector if needed
    if table:
        for row in table.find_all("tr")[1:]:  # Skip the header
            cols = row.find_all("td")
            if len(cols) > 0:
                data = {
                    "Date": cols[0].text.strip(),
                    "Time": cols[1].text.strip(),
                    "Magnitude": cols[2].text.strip(),
                    "Location": cols[3].text.strip(),
                }
                earthquakes.append(data)
    
    return earthquakes

def napoli_check(data):
    # Filter earthquakes that occurred in Napoli
    napoli_earthquakes = [quake for quake in data if "Napoli" in quake.get("Location", "")]
    state = False
    if napoli_earthquakes:
        state = True
        print("🌍 Earthquakes detected in Napoli:")
        for quake in napoli_earthquakes:
            print(f"📅 Date: {quake['Date']} | ⏰ Time: {quake['Time']} | 💥 Magnitude: {quake['Magnitude']} | 📍 Location: {quake['Location']}")
    else:
        print("✅ No recent earthquakes detected in Napoli.")

    return state

data = scrape_ingv_earthquakes()
state = napoli_check(data)
    