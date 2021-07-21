from requests import exceptions as reqex
from urllib3 import exceptions as urlibex
import argparse
import requests
import json

print("""

\033[36m┬ ┬┌┬┐┌┬┐┌─┐  ┌─┐┌─┐┬ ┬┬  ┌─┐┌─┐┌┬┐
\033[35m├─┤ │  │ ├─┘  ├─┘├─┤└┬┘│  │ │├─┤ ││
\033[36m┴ ┴ ┴  ┴ ┴    ┴  ┴ ┴ ┴ ┴─┘└─┘┴ ┴─┴┘
\033[35m[+] Checking HTTP Request for Http Injector BUG
\033[36m[+] Created by: FachrulRH
""")

parser = argparse.ArgumentParser()

parser.add_argument("--url", help="Target url i.e http://www.bug.com")
parser.add_argument("--proxy", help="Insert squid proxy i.e user:pass@ip:host or ip:host")
parser.add_argument("--file", help="Using target file")
parser.add_argument("--result", help="Result target path")

args = parser.parse_args()

if args.url is None and args.file is None:
    print("\033[31m[-] Argument --url or --file not found, see httpay.py -h for help")
    quit(0)

if args.result != None:
    o = open(args.result, 'w+')
else:
    o = open("result.txt", 'w+')


def proxy_request(proxy, target=None, file=None):
    if target is not None:
        # Check http request with proxy method
        get_proxy_request(target, proxy)
    elif file is not None:
        # Checking many bug in same time with proxy method
        with open(file, 'r') as targets:
            for target in targets:
                target = str(target.replace("\n", ""))
                get_proxy_request(target, proxy)

def direct_request(target=None, file=None):
    # Check http request with direct method
    if target is not None:
        get_direct_request(target.strip())
    elif file is not None:
        # Checking many bug in same time with direct method
        with open(file, 'r') as targets:
            for target in targets:
                try:
                    target = str(target.replace("\n", ""))
                    get_direct_request(target.strip())
                except ConnectionRefusedError:
                    print("\033[31m[+] ErrorConnection Refused")

def save_request(result, target):
    headers = json.dumps(dict(result), indent=1)
    o.write('-'*100 + '\n')
    o.write('Target: ' + target + '\n')
    o.write(headers + '\n')

def check_status_code(r, target):
    if r.status_code == 200:
        print("\033[36m" + target)
        print("\033[32mResult: " + "200 OK")
    elif r.status_code == 302:
        print("\033[36m" + target)
        print("\033[33mResult: " + "302 Redirect")
        print("\033[33mLocation: " + r.headers['Location'])
    elif r.status_code == 301:
        print("\033[36m" + target)
        print("\033[33mResult: " + "301 Redirect")
        print("\033[33mLocation: " + r.headers['Location'])
    else:
        print("\033[36m" + target)
        print("\033[31mResult: " + r.status_code)

def get_direct_request(target):
    r = requests.get(target, allow_redirects=False)
    check_status_code(r, target)
    save_request(r.headers, target)

def get_proxy_request(target, proxy):
    r = requests.get(target, allow_redirects=False, proxies=proxy)
    check_status_code(r, target)
    save_request(r.headers, target)

if (args.proxy is not None):
    try:
        proxy = {
            "http": "http://" + args.proxy, 
            "https": "https://" + args.proxy 
        }
        print("\033[32m[+] Start checking the request...")
        print("\033[33m[!] It may takes a long time...")
        print("\033[33m[!] You can quit by pressing CTRL+C")        
        proxy_request(proxy, args.url, args.file)
    except KeyboardInterrupt:
        print("\033[31m[-] KeyboardInterrupt System Quit...")    
        quit(0)    
else:
    try:
        print("\033[32m[+] Start checking the request...")
        print("\033[33m[!] Proxy argument not found using direct method\033[36m")
        direct_request(args.url, args.file)
    except KeyboardInterrupt:
        print("\033[31m[-] KeyboardInterrupt System Quit...")    
        quit(0)  