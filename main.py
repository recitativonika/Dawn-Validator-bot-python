import requests
import random
import time
import yaml
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter('ignore', InsecureRequestWarning)

with open('./config.yaml') as f:
    config = yaml.safe_load(f)

with open('./accounts.yaml') as f:
    accounts_data = yaml.safe_load(f)['accounts']

with open('./proxy.yaml') as f:
    proxies = yaml.safe_load(f)['proxies']

api_endpoints = {
    "keepalive": "https://www.aeropres.in/chromeapi/dawn/v1/userreward/keepalive",
    "getPoints": "https://www.aeropres.in/api/atom/v1/userreferral/getpoint"
}

def random_delay(min_seconds, max_seconds):
    delay_time = random.randint(min_seconds, max_seconds)
    time.sleep(delay_time)

def display_welcome():
    print("""
 -----------------------------------------------
|🌟 DAWN Validator Extension automatic claim 🌟|
 -----------------------------------------------
    """)

def fetch_points(headers):
    try:
        response = requests.get(api_endpoints['getPoints'], headers=headers, verify=False)
        if response.status_code == 200 and response.json().get("status"):
            data = response.json()["data"]
            reward_point = data["rewardPoint"]
            referral_point = data["referralPoint"]
            total_points = (
                reward_point.get("points", 0) +
                reward_point.get("registerpoints", 0) +
                reward_point.get("signinpoints", 0) +
                reward_point.get("twitter_x_id_points", 0) +
                reward_point.get("discordid_points", 0) +
                reward_point.get("telegramid_points", 0) +
                reward_point.get("bonus_points", 0) +
                referral_point.get("commission", 0)
            )
            print(f"\n📊 Points: {total_points}")
            return total_points
        else:
            print(f"❌ Failed to retrieve points: {response.json().get('message', 'Unknown error')}")
    except Exception as e:
        print(f"⚠️ Error during fetching points: {str(e)}")
    return 0

def keep_alive_request(headers, email):
    payload = {
        "username": email,
        "extensionid": "fpdkjdnhkakefebpekbdhillbhonfjjp",
        "numberoftabs": 0,
        "_v": "1.0.8"
    }
    
    try:
        response = requests.post(api_endpoints["keepalive"], json=payload, headers=headers, verify=False)
        if response.status_code == 200:
            print(f"✅ Keep-Alive Success for {email}: {response.json().get('message')}")
            return True
        else:
            print(f"🚫 Keep-Alive Error for {email}: {response.status_code} - {response.json().get('message', 'Unknown error')}")
    except Exception as e:
        print(f"⚠️ Error during Keep-Alive: {str(e)}")
    return False

def countdown(seconds, message):
    for i in range(seconds, 0, -1):
        print(f"⏳ {message} in: {i} seconds...", end='\r')
        time.sleep(1)
    print("\n🔄 Restarting...\n")

def countdown_account_delay(seconds):
    for i in range(seconds, 0, -1):
        print(f"⏳ Waiting for account processing in: {i} seconds...", end='\r')
        time.sleep(1)
    print("\n")

def process_accounts():
    display_welcome()
    total_proxies = len(proxies)

    while True:
        total_points = 0

        for i, account in enumerate(accounts_data):
            email = account['email']
            token = account['token']
            proxy = proxies[i % total_proxies] if config["useProxy"] else None

            headers = {
                "Accept": "*/*",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
            }

            if proxy:
                headers['Proxy'] = proxy
            
            print("----------------------------------------------------------------")
            print(f"🔍 Processing: {email} using proxy: {proxy or 'No Proxy'}...")
            points = fetch_points(headers)
            total_points += points

            if points > 0:
                success = keep_alive_request(headers, email)
                if not success:
                    print(f"✅ Keep-Alive Success for {email} account.\n")
            else:
                print(f"❌ No points available for {email}.")
                print("----------------------------------------------------------------")

            countdown_account_delay(config["accountDelay"])

        print(f"📋 All accounts processed. Total points: {total_points}")
        countdown(config["restartDelay"], "Next process")

if __name__ == "__main__":
    process_accounts()
