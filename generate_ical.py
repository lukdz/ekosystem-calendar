import os
import sys
import json
import requests
import re
import urllib.parse
import html
import datetime
import uuid
from icalendar import Calendar, Event, Alarm, vText

# Emoji and naming mapping
# As requested, BIO is 🟤 (Brown circle)
TYPE_MAPPING = {
    "papier": "🔵 Paper",
    "szkło": "🟢 Glass",
    "tworzywa": "🟡 Plastics & Metals",
    "BIO": "🟤 Bio Waste",
    "zmieszane": "⚫ Mixed Waste"
}

def fetch_schedule(id_ulicy, id_numeru):
    url = "https://ekosystem.wroc.pl/wp-admin/admin-ajax.php"
    payload = {
        "action": "waste_disposal_form_get_schedule_direct",
        "id_ulicy": id_ulicy,
        "id_numeru": id_numeru
    }
    
    response = requests.post(url, data=payload)
    response.raise_for_status()
    data = response.json()
    
    wiadomosc = data.get("wiadomosc", "")
    if not wiadomosc:
        raise ValueError("No 'wiadomosc' field found in response.")
    
    match = re.search(r'href="([^"]+)"', wiadomosc)
    if not match:
        raise ValueError("Could not extract URL from 'wiadomosc'.")
        
    extracted_url = match.group(1)
    decoded_url = html.unescape(extracted_url)
    
    parsed_url = urllib.parse.urlparse(decoded_url)
    query_params = urllib.parse.parse_qsl(parsed_url.query)
    
    schedule_dict = {}
    
    for key, value in query_params:
        if key.startswith("kiedy_"):
            idx = key.split("_")[1]
            if idx not in schedule_dict:
                schedule_dict[idx] = {}
            schedule_dict[idx]["date"] = value
        elif key.startswith("co_"):
            idx = key.split("_")[1]
            if idx not in schedule_dict:
                schedule_dict[idx] = {}
            schedule_dict[idx]["type"] = value
            
    schedule_list = []
    for idx in sorted(schedule_dict.keys(), key=lambda x: int(x)):
        event = schedule_dict[idx]
        if "date" in event and "type" in event:
            schedule_list.append({
                "date": event["date"],
                "type": event["type"]
            })
            
    return schedule_list

def get_event_summary(waste_type):
    return TYPE_MAPPING.get(waste_type, f"⚪ {waste_type.capitalize()}")

def create_calendar(schedule):
    cal = Calendar()
    cal.add('prodid', '-//Ekosystem Wroclaw Calendar//EN')
    cal.add('version', '2.0')
    cal.add('x-wr-calname', 'Garbage Collection')
    cal.add('x-wr-timezone', 'Europe/Warsaw')

    for item in schedule:
        date_str = item["date"]
        waste_type = item["type"]
        
        event_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        summary = get_event_summary(waste_type)
        
        event = Event()
        event.add('summary', summary)
        # For an all-day event, we pass the date object directly.
        # icalendar will format it properly as DTSTART;VALUE=DATE:YYYYMMDD
        event.add('dtstart', event_date)
        # End date is exclusive in iCal (next day)
        event.add('dtend', event_date + datetime.timedelta(days=1))
        
        # Stable UID based on date and type so it doesn't duplicate on refresh
        uid_string = f"{date_str}-{waste_type}@ekosystem-calendar"
        # We can just hash or use the string directly if valid
        event.add('uid', uid_string)
        
        # Add timestamp of creation
        event.add('dtstamp', datetime.datetime.now(datetime.timezone.utc))

        # Notification logic: "all day" with reminder the evening before at 18:00
        # Since the all-day event technically starts at 00:00 on event_date,
        # a trigger of -6 hours (-PT6H) places the alarm exactly at 18:00 the day before.
        # This keeps the code clean and easily modifiable later if needed.
        alarm = Alarm()
        alarm.add('action', 'DISPLAY')
        alarm.add('description', f"Reminder: {summary} collection tomorrow!")
        alarm.add('trigger', datetime.timedelta(hours=-6))
        
        event.add_component(alarm)
        cal.add_component(event)
        
    return cal

def main():
    locations_json = os.environ.get("LOCATIONS_JSON")
    
    if not locations_json:
        print("Error: LOCATIONS_JSON environment variable must be set.")
        sys.exit(1)
        
    try:
        locations = json.loads(locations_json)
    except Exception as e:
        print(f"Error parsing LOCATIONS_JSON: {e}")
        sys.exit(1)

    os.makedirs("public", exist_ok=True)

    for key, loc in locations.items():
        street_id = loc.get("streetId")
        house_id = loc.get("houseId")
        
        if not street_id or not house_id:
            print(f"Skipping invalid entry at key {key}: {loc}")
            continue

        print(f"Fetching schedule for location {key}")
        try:
            schedule = fetch_schedule(street_id, house_id)
            print(f"Fetched {len(schedule)} events.")
        except Exception as e:
            print(f"Failed to fetch schedule for location {key}: {e}")
            continue
            
        cal = create_calendar(schedule)
        
        output_filename = f"public/calendar_{key}.ics"
        with open(output_filename, 'wb') as f:
            f.write(cal.to_ical())
            
        print(f"Successfully generated {output_filename}")

if __name__ == "__main__":
    main()
