# DAWN Validator Extension automatic claim
  Python version of Dawn Validator Bot

## What needed
- Python

## Features

- Automatically send keep-alive requests to claim points.
- Multi-account.
- Auto loop.
- Proxy support.


## Installing and setup

### Install
1. Clone the project and go to project directory
   ```
   git clone https://github.com/recitativonika/Dawn-Validator-bot-python.git
   ```
   ```
   cd Dawn-Validator-bot-python
   ```
2. Install required package
   ```
   pip install -r requirements.txt
   ```
### Setup and run

1. Login/register Dawn Validator account and login, get the token in "getpoint?appid=" -> "authorization:" at network tab in inspect element in browser. 
2. In `Dawn-Validator-bot-python` directory, Edit and adjust this line in `accounts.yaml` and save it
```
  accounts:
    - email: "account1@example.com"     # Replace with actual email
      token: "example_token_1"           # Replace with actual token
    - email: "account2@example.com"
      token: "example_token_2"
    # Add more accounts as needed
```
3. Edit and adjust the `config.yaml` for proxy and delay options.
```
  useProxy: false          # Set to true if you want to use proxies, false otherwise
  accountDelay: 121        # Delay in seconds for processing each account
  restartDelay: 241       # Delay in seconds for restarting the processing loop
```
4. Edit the `proxy.yaml` if you want to use proxy
5. Run the script to start, use :
    ```
    python main.py
    ```
	
	
	
Dawn Validator Extension : https://chromewebstore.google.com/detail/dawn-validator-chrome-ext/fpdkjdnhkakefebpekbdhillbhonfjjp?authuser=0&hl=en

My reff code if you want :) : 9lv10g33
