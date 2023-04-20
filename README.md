Dependencies:
-  An account at https://support.maxmind.com/hc/en-us/articles/4407099783707-Create-an-Account
-  -Download the geolite2-city.mmdb from https://www.maxmind.com/en/accounts/854495/geoip/downloads
- API Key from https://www.abuseipdb.com/ for AbuseIPDB lookups

threatCheck.py does the following:

-    It reads a list of IP addresses from a file named "logs/blocked-ips.log".
-    It initializes a MaxMind GeoIP2 database by opening a file named "geolite2-city.mmdb".
-    It initializes Pygame mixer to play audio.
-    It sets a threshold value for a threat level at 50.
-    It iterates over the list of IP addresses and performs the following actions for each IP address
--        It uses the MaxMind database to obtain the geolocation information for the IP address.
--        It sends a request to the AbuseIPDB API to obtain the abuse information for the IP address.
--        It logs the geolocation information, abuse information, and threat level for the IP address.
--        If the threat level is above the threshold value, it logs a message indicating a potential threat has been detected and plays an audible alert.
--    It closes the MaxMind database.
--    It empties the contents of the file "logs/blocked-ips.log".

Overall, this is a simple implementation of a threat detection system that uses geolocation and abuse information to determine whether an IP address poses a potential threat. If a threat is detected, an audible alert is played and the information is logged.

Note that this code is designed to run continuously and process any new IP addresses added to the "blocked-ips.log" file. It is assumed that some external process is responsible for adding IP addresses to the file, such as a firewall or intrusion detection system.
