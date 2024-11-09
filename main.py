import requests
import yaml
import time
import random
import ssl
import asyncio
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter('ignore', InsecureRequestWarning)

with open('config.yaml') as config_file:
    config = yaml.safe_load(config_file)

with open('accounts.yaml') as accounts_file:
    accounts_data = yaml.safe_load(accounts_file)

with open('proxy.yaml') as proxy_file:
    proxy_data = yaml.safe_load(proxy_file)

proxies = proxy_data.get('proxies', [])

if not isinstance(proxies, list):
    raise ValueError("Proxies must be a list under the 'proxies' key")

api_endpoints = {
    "keepalive": "https://www.aeropres.in/chromeapi/dawn/v1/userreward/keepalive",
    "getPoints": "https://www.aeropres.in/api/atom/v1/userreferral/getpoint"
}

ssl._create_default_https_context = ssl._create_unverified_context

def random_delay(min_seconds, max_seconds):
    delay_time = random.randint(min_seconds, max_seconds)
    time.sleep(delay_time)

def display_welcome():
    print("""
                \x1b[32m🌟 DAWN Validator Extension automatic claim 🌟\x1b[0m
                          \x1b[36mGithub: recitativonika\x1b[0m
                        \x1b[36mgithub.com/recitativonika\x1b[0m
    """)

async def fetch_points(headers):
    try:
        response = requests.get(api_endpoints["getPoints"], headers=headers, verify=False)
        if response.status_code == 200 and response.json().get('status'):
            data = response.json().get('data', {})
            reward_point = data.get('rewardPoint', {})
            referral_point = data.get('referralPoint', {})
            total_points = (
                reward_point.get('points', 0) +
                reward_point.get('registerpoints', 0) +
                reward_point.get('signinpoints', 0) +
                reward_point.get('twitter_x_id_points', 0) +
                reward_point.get('discordid_points', 0) +
                reward_point.get('telegramid_points', 0) +
                reward_point.get('bonus_points', 0) +
                referral_point.get('commission', 0)
            )
            return total_points
        else:
            print(f"❌ Failed to retrieve the points: {response.json().get('message', 'Unknown error')}")
    except Exception as error:
        print(f"⚠️ Error during fetching the points: {error}")
    return 0

async def keep_alive_request(headers, email):
    payload = {
        "username": email,
        "extensionid": "fpdkjdnhkakefebpekbdhillbhonfjjp",
        "numberoftabs": 0,
        "_v": "1.0.9"
    }
    
    try:
        response = requests.post(api_endpoints["keepalive"], json=payload, headers=headers, verify=False)
        if response.status_code == 200:
            return True
        else:
            print(f"🚫 Keep-Alive Error for {email}: {response.status_code} - {response.json().get('message', 'Unknown error')}")
    except Exception as error:
        print(f"⚠️ Error during keep-alive request for {email}: {error}")
    return False

async def process_account(account, proxy):
    email = account['email']
    token = account['token']
    
    headers = {
        "Accept": "*/*",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    }

    if proxy:
        headers['Proxy'] = proxy

    points = await fetch_points(headers)

    print(f"🔍 Processing: \x1b[36m{email}\x1b[0m, Proxy: {'\x1b[33m' + proxy + '\x1b[0m' if proxy else '\x1b[33mNo Proxy\x1b[0m'}, Points: \x1b[32m{points}\x1b[0m")

    success = await keep_alive_request(headers, email)
    if success:
        print(f"✅ Keep-Alive Success for: \x1b[36m{email}\x1b[0m")
    else:
        print(f"⚠️ Error during keep-alive request for \x1b[36m{email}\x1b[0m: Request failed with status code 502")
        print(f"❌ Keep-Alive Failed for: \x1b[36m{email}\x1b[0m")

    return points

async def countdown(seconds):
    for i in range(seconds, 0, -1):
        print(f"⏳ Next process in: {i} seconds...", end='\r')
        await asyncio.sleep(1)
    print("\n🔄 Restarting...\n")

async def process_accounts():
    display_welcome()
    total_proxies = len(proxies)

    while True:
        account_promises = []

        for index, account in enumerate(accounts_data):
            proxy = proxies[index % total_proxies] if config.get('useProxy') else None
            account_promises.append(process_account(account, proxy))

        points_array = await asyncio.gather(*account_promises)
        total_points = sum(points_array)

        print(f"📋 All accounts processed. Total points: \x1b[32m{total_points}\x1b[0m")
        await countdown(config['restartDelay'])

if __name__ == "__main__":
    try:
        asyncio.run(process_accounts())
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting gracefully.")
