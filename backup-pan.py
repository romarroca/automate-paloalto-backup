import requests
import datetime
import os

# Palo Alto Firewall Credentials
ip = "10.1.1.1"   # Change to your firewall IP
username = "admin"        # Change to your username
password = "admin"     # Change to your password
BACKUP_DIR = "./backups"  # Directory to store backups

# Disable SSL warnings (not recommended for production)
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


def get_api_key(ip, username, password):
    """Fetch API key from Palo Alto firewall."""
    url = f'https://{ip}/api/?type=keygen&user={username}&password={password}'
    response = requests.get(url, verify=False)
    
    if "<key>" in response.text:
        return response.text.split("<key>")[1].split("</key>")[0]
    else:
        print("Error: Unable to retrieve API key.")
        exit(1)

def backup_config(ip, api_key):
    """Export Device State"""
    url = f"https://{ip}/api/?type=export&category=device-state&key={api_key}"

    # Create backup directory if it doesn't exist
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    # Generate timestamp for filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"{BACKUP_DIR}/config_{timestamp}.tgz"

    response = requests.get(url, verify=False)

    if response.status_code == 200:
        with open(backup_filename, "wb") as file:
            file.write(response.content)
        print(f"Backup saved: {backup_filename}")
    else:
        print("Error: Failed to download the configuration.")

def main():
    api_key = get_api_key(ip, username, password)
    backup_config(ip, api_key)

if __name__ == "__main__":
    main()
