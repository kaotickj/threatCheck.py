import datetime
import pygame
import maxminddb
import requests


# Load IP addresses from file
ip_file = 'logs/blocked-ips.log'
try:
    with open(ip_file, 'r') as f:
        ips = f.read().splitlines()
except FileNotFoundError:
    print(f"Error: {ip_file} not found")
    exit()

# Check if the file is empty
if not ips:
    print("Blocked IPs log file is empty. Exiting...")
    exit()

# Initialize geolocation database
try:
    reader = maxminddb.open_database('geolite2-city.mmdb')
except FileNotFoundError:
    print("Error: geolite2-city.mmdb not found")
    exit()

# Initialize Pygame mixer for playing audio
try:
    pygame.mixer.init()
except pygame.error as e:
    print(f"Error: {e}")
    exit()

# Set threat threshold to 50
THREAT_THRESHOLD = 50

# Iterate over IP addresses
for ip in ips:
    # Get geolocation information
    try:
        geo_info = reader.get(ip)
    except ValueError:
        print(f"Error: Invalid IP address - {ip}")
        continue
    except (maxminddb.errors.InvalidDatabaseError, maxminddb.errors.AddressNotFoundError) as e:
        print(f"Error: {e}")
        continue

    # Get abuse information
    url = f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip}"
    headers = {
        "Key": "YOUR_API_KEY_HERE",
        "Accept": "application/json"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"Error: {e}")
        continue
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        continue
    abuse_info = response.json()['data']

    # Log results
    print(f"IP address: {ip}")
    try:
        geolocation = f"{geo_info['city']['names']['en']}, {geo_info['subdivisions'][0]['iso_code']}, {geo_info['country']['iso_code']}"
        print(f"Geolocation: {geolocation}")
    except KeyError:
        print("Error: Invalid geolocation data")
        continue
    print(f"Threat level: {abuse_info['abuseConfidenceScore']}")

    if abuse_info['abuseConfidenceScore'] > THREAT_THRESHOLD:
        print(f"ALERT: Potential threat detected from {ip}!")
        with open('logs/known_threats.log', 'a') as f:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{timestamp} {ip} {geolocation} {abuse_info['abuseConfidenceScore']}\n")
        # Play audible alert
        try:
            pygame.mixer.music.load("alert.oga")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pass
        except pygame.error as e:
            print(f"Error: {e}")

# Close geolocation database
reader.close()

# Delete contents of logs/blocked-ips.log
with open(ip_file, 'w'):
    pass
