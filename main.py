import os
import socket
import requests
import time
import whois
import urllib.parse
import subprocess
import sys
import hashlib
from cryptography.fernet import Fernet
import random
from pyfiglet import Figlet
import exifread
import base64
import string
import webbrowser
import tkinter as tk



def show_website_tiktok():
    webbrowser.open('https://glitch-tools.netlify.app')
    webbrowser.open('https://tiktok.com/@glitch_blackhat')

ports = [22, 21, 20, 23, 25, 53, 67, 68, 69, 80, 110, 123, 139, 143, 161, 443, 445, 3389]
def port_scanner():
    target = input("Enter Target IP or Domain: ")
    for port in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)

            res = s.connect_ex((target, port))

            if res == 0:
                print(f'[+] Port {port} is open')
            else:
                print(f'[-] Port {port} is closed')
        except KeyboardInterrupt:
            print('ctrl + c detected Exiting...')
        finally:
            s.close()



def ping():
    target = input("Enter Target IP or Domain: ")
    try:
        res = subprocess.run(["ping", target], capture_output=True)

        if res.returncode == 0:
            print('Target reachable')
        else:
            print("Target not reachable")
    except KeyboardInterrupt:
        print('ctrl + c detected Exiting...')





def dns():
    hostname = input('Enter hostname exmp(google.com): ')
    try:
        ip_address = socket.gethostbyname(hostname)
        print("Getting IP...")
        time.sleep(3)
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"IP address of {hostname}: {ip_address}")
    except socket.gaierror as e:
        print(f"Error resolving {hostname}: {e}")




def dirb():
    target = input('Enter Target url: ')
    word_list = input('Enter list you want to use if you dont have one use(dirb.txt): ')
    try:
        with open(word_list, 'r') as f:
            words = f.read().splitlines()

        for word in words:
            full_url = f'{target}/{word}'

            data = requests.get(full_url, timeout=3)

            if data.status_code == 200:
                print(f'200 --> Found {full_url}')
            elif data.status_code == 301 or data.status_code == 302:
                print(f'{data.status_code} --> Redirected: {full_url}')
            elif data.status_code == 403:
                print(f'Forbidden --> {full_url}')
            elif data.status_code == 404:
                print(f'Not found --> {full_url}')
            else:
                pass
    except KeyboardInterrupt:
        print('ctrl + c detected Exiting...')





def rate_limit_tester():
    warning = input('If the rate limit test seems to be slow. That means that your network communication is slow or The server protects him self well Press enter to continue: ')
    os.system('cls' if os.name == 'nt' else 'clear')
    target = input('Enter target IP or url: ')
    request_max = int(input('Enter how much requests to send exmp(50): '))

    for i in range(request_max):
        resp = requests.get(target, timeout=3)

        print(f'Request {i+1} == {resp.status_code}')

        if resp.status_code == 429:
            print(f'Rate limit got hit after {i+1} requests.')
            reset_time = resp.headers.get('Retry-After')

            if reset_time:
                print(f"New requests in {reset_time} seconds allowed.")
            break
        elif resp.status_code == 503:
                print(f'Server temporarily unavailable (503) after {i+1} requests.')
                break

        time.sleep(0.2)


def reverse_dns():
    ip = input("Enter IP address: ")
    
    try:
        result = socket.gethostbyaddr(ip)
        print("Hostname:", result[0])
        print("Aliases:", result[1])
        print("IP list:", result[2])
    
    except socket.herror:
        print("No reverse DNS entry found")




def ip_geo():

    ip = input("IP: ")

    

    r = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
    print(r.json())

    with open('Ip-Geolocate-info.txt', 'w') as f:
        f.write(str(r.json()))
        
    print('Info saved to Ip-Geolocate-info.txt')




def subfinder():
    
    target = input('Enter Domain not url: ')
    protocol = input('Enter protocol for the website you choose (https/http): ')
    subdomains = [
    "www", "mail", "api", "dev", "test", "beta", "ftp", "blog", "shop", "admin", "portal",
    "m", "webmail", "static", "cdn", "support", "secure", "devops", "monitor", "status", "staging",
    "files", "downloads", "docs", "cloud", "intranet", "calendar", "store", "news", "contact", "help",
    "sms", "ads", "crm", "push", "dev2", "images", "video", "file", "content", "support2", "customers",
    "api2", "auth", "gateway", "signin", "signup", "management", "public", "private", "resource", 
    "v1", "v2", "v3", "ssl", "adminpanel", "backend", "dashboard", "reports", "updates", "events",
    "data", "analytics", "apps", "app", "app2", "ticket", "verify", "appstore", "storefront", 
    "api-dev", "production", "test2", "test3", "sandbox", "helpdesk", "employees", "hr", "accounting",
    "login", "admin1", "admin2", "portal2", "enterprise", "public-api", "private-api", "api-test",
    "members", "partners", "partner", "corporate", "client", "clients", "projects", "services", "tools"
]
    session = requests.Session()

    for domain in subdomains:
        url = f'{protocol}://{domain}.{target}'

        
        try:
            resp = session.get(url, timeout=10)
            
            if resp.status_code in [200, 301, 302, 403, 401]:
                print(f'Sub domain found --> {url}')
                with open('Found-Subdomain.txt', 'a') as f:
                    f.write(f'Subdomain found ----> {url}\n')
            else:
                print(f"[?] {resp.status_code} --> {url}")
        except requests.exceptions.RequestException as e:
            print(f'[-] subdomain {domain} does not resolve ')
        
    print('Found Subdomains were added to Found-Subdomain.txt')



def whois_lookup():
    target = input('Enter domain: ')
    w = whois.whois(target)
    print(w)


def search_robots():
    
    target = input('Enter target url: ')
     
    url = f'{target}/robots.txt'

    data = requests.get(url, timeout=3)
    
    if data.status_code == 200:
        print(f'[+] Successfull found robots.txt --> {url}')
    else:
        print(f'[-] No robots.txt file was found {url}')



def simple_fuzzing():
    warning = input("[INFO] No output does not necessarily mean the target is secure. Press Enter to continue. ")
    target = input('Enter target url: ')

    fuzzing_payloads = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    '<iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/771984076&color=%23ff5500&auto_play=true&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true"></iframe>',
    "' OR 1=1 --",
    "' UNION SELECT null, null, null, null --",
    "<svg/onload=alert('XSS')>",
    "' OR 'a'='a",
    "; DROP TABLE users;",
    "<body onload=alert('XSS')>",
    "' or 1=1;--",
    "<svg><script>alert('XSS')</script></svg>",
    "<svg><image src='x' onerror='alert(\"XSS\")'></svg>",
    "' DROP DATABASE mydb; --",
    "<iframe src='javascript:alert('XSS');'></iframe>",
    "%00", 
    "../../../../etc/passwd",
    "../../../../etc/shadow",
    "../../../bin/bash",
    "../../../var/www/html/index.php",
    "..\\..\\..\\..\\..\\windows\\system32\\config",
    "..%5C..%5C..%5C..%5C..%5Cetc%5Cpasswd",
    "<script src='http://malicious.com/malicious.js'></script>",
    "</script><img src='x' onerror='alert('XSS')'>",
    "<img src='x' onerror='alert(1)'>",
    "<svg><script>alert('XSS')</script></svg>",
    "<script>alert('XSS')</script>",
    "<svg onload=alert(1)>",
    "; ls",
    "; id",
    "; whoami",
    "; uname -a",
    "; cat /etc/passwd",
    
]
    for payload in fuzzing_payloads:
        encoded = urllib.parse.quote(payload)
        url = f'{target}?q={encoded}'

        try:
            resp = requests.get(url, timeout=3)

            print(f'Testing: {payload}')

            if urllib.parse.quote(payload) in resp.text:
                print(f"[!] Possible vulnerability found with payload: {payload} --> {url}")


            if encoded in resp.text:
                print("  [!] Reflected (encoded)")
            
            if resp.status_code >= 500:
                print('[!] Server Error')

        except requests.exceptions.RequestException:
            print("[!] Request failed")





def md5_hash():
    

    warning = input('[Info] after hashing this text you cannot crack it with this tool. You have to search online for tools to crack it. Press Enter to continue: ')
    inp = input('Enter text or password to hash: ')
    
    hashed = hashlib.md5(inp.encode()).hexdigest()
    print('Hashed Text: ',hashed)




def sha256():
    warning = input('[Info] after hashing this text you cannot crack it with this tool. You have tp search online for tools to crack it. Press Enter to continue: ')
    inp = input('Enter text or password to hash: ')
    
    hashed = hashlib.sha256(inp.encode()).hexdigest()
    print('Hashed Text: ',hashed)



def passwd_gen():
    inp_len = int(input('Enter the lenght you want fpr the password (32 characters is maximum): '))


    if inp_len > 32:
        print('Entered lenght longer than maximum lenght.')
        return
    else:
        pass

    chars = 'asdfghlöäyxcvbnm,.-12345678ß!"§$%&/()=?#@qwertzuiopü_'

    for times in range(5):
        passwd_encr = ''.join(random.choice(chars) for i in range(inp_len))

        print('Created passwd: ', passwd_encr)


def enc():
    try:

        inp = str(input('Enter path to the file you want to encrypt: '))
    except ValueError:
        print('Enter the full path without any numbers: ')
        return

    with open(inp, 'rb') as file_binary:
        data = file_binary.read()

        encrypted_data = f.encrypt(data)

    with open(inp, 'wb') as file_binary:
        file_binary.write(encrypted_data)

        

def decrypt():
         
    try:
        inp = str(input('Enter path to the file you want to encrypt: '))

    except ValueError:

        print('Enter the full path without any numbers: ')
        return

    with open(inp, 'rb') as file_binary:
        data = file_binary.read()

        decrypted_data = f.decrypt(data)

        with open(inp, 'wb') as file_binary:
            file_binary.write(decrypted_data)



def file_encryption():
    global f
    # DO NOT CHANGE THIS KEY YOU COULD NOT ENCRYPT ANY FILES; OR IF YOU HAVE ENCRYPTED FILES WITH THIS TOOL, YOU CANT DECRYPT THEM
    #=========================================================
    key = 'uCmn2eKxres0Cy8WhzXA7BFWUChx6FapMrR2POIYG7Y='
    #=========================================================

    f = Fernet(key)

    
    try:
        warning = input('[INFO] You can only decrypt files that has been encrypted with this tool before.  e = encrypt, d = decrypt')
        choose = input('Do you want to encrypt a file or decrypt a file that has been encrypted with this tool? choose(e/d): ')
    except ValueError:
        print('You have to enter e or d. e = encrypt, d = decrypt ')
        return
    
    if choose == 'e':
        enc()

    elif choose == 'd':
        decrypt()

    

def note():
    note_text = input('Enter a note to save for later: ')

    with open('Note.txt', 'a') as f:
        f.write(note_text)

    print('Your note have been saved to Note.txt')


def  reverse_text():
    inp = input('Enter text to reverse: ')
    print(f'Reversed text: {inp[::-1]}')


def google_dorks():
    warning = input('[INFO] This google dork tool will not do a goolgle search,\nIt will give you the full link of the dork, so you can visit it. exmp(https://google.com/search?q=Dork...)  Press enter to continue')


    google_dorks = [
    # Login Panels
    'intitle:"login"',
    'inurl:admin/login',
    'intitle:"admin panel"',
    'inurl:wp-admin',
    'inurl:administrator',

    # Open Directories
    'intitle:"index of"',
    'intitle:"index of" "backup"',
    'intitle:"index of" "config"',
    'intitle:"index of" passwd',
    'intitle:"index of" ".git"',

    # Exposed Files
    'filetype:env DB_PASSWORD',
    'filetype:sql "INSERT INTO"',
    'filetype:log password',
    'filetype:bak inurl:backup',
    'ext:xml inurl:sitemap',

    # Sensitive Documents
    'filetype:pdf confidential',
    'filetype:xls username password',
    'filetype:docx internal use only',
    'filetype:txt password',
    'filetype:csv email',

    # Cameras / IoT
    'inurl:view/view.shtml',
    'intitle:"webcamXP 5"',
    'inurl:"ViewerFrame?Mode="',
    'intitle:"Live View / - AXIS"',
    'server:SQ-WEBCAM',

    # SQL Errors
    '"sql syntax near"',
    '"mysql_fetch_array()"',
    '"ORA-00933"',
    '"ODBC SQL Server Driver"',
    '"Unclosed quotation mark after the character string"',

    # Exposed Configs
    'filetype:env APP_KEY',
    'filetype:ini password',
    'filetype:yaml api_key',
    'filetype:json "auth_token"',
    'filetype:config db_password',

    # Git / Dev Files
    'inurl:.git/config',
    'inurl:.env',
    'inurl:package.json',
    'inurl:composer.json',
    'inurl:webpack.config.js',

    # Cloud / Storage
    'site:s3.amazonaws.com confidential',
    'site:blob.core.windows.net password',
    'site:drive.google.com "index of"',
    'site:pastebin.com api_key',
    'site:github.com "AWS_SECRET_ACCESS_KEY"',

    # Webcams / Printers
    'intitle:"printer status"',
    'intitle:"network camera"',
    'inurl:/cgi-bin/',
    'intitle:"HP LaserJet"',
    'intitle:"Web Image Monitor"',

    # Misc
    'site:example.com ext:php',
    'cache:example.com',
    'related:example.com',
    'info:example.com',
    'link:example.com'
]
    

    print('All google dork links you can visit:\n ')


    for dork in google_dorks:
        encoded = urllib.parse.quote(dork)
        print(f"Visit: https://www.google.com/search?q={encoded}")
        time.sleep(0.5)






def ascii_art_gen():
    inp = input('Enter word that should be transformed into ascii art. Exmp(Your first Name): ')

    fonts = ["slant", "banner3-D", "doom", "big", "standard", "bloody", "poison", "ghost", "graffiti"]

    for font in fonts:
        f = Figlet(font=font)
        print(f.renderText(inp))





def tiktok_username_search():
    inp = input('Enter username to search on tiktok with or without @: ').strip()

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/122.0 Safari/537.36"
        )
    }

    username = inp.replace('@', '')
    url = f'https://www.tiktok.com/@{username}'


    try:
        r = requests.get(url, headers=headers, timeout=30, allow_redirects=True)

        final_url = r.url.lower()

        if "/404" in final_url:
            print(f"[-] Username not found: @{username}")

        elif r.status_code == 200:
            print(f"[+] Username exists: {url}")

        else:
            print(f"[!] Status code: {r.status_code}")

    except requests.exceptions.RequestException as e:
        print(f'[!] Error: {e}')


def insta_username_search():
    warning = input('[INFO] This tool might give you that the username is available, sometimes its wrong! Press enter to continue: ')
    inp = input('Enter username to search on Instagram: ').strip()

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/122.0 Safari/537.36"
        )
    }

    url = f'https://www.instagram.com/{inp}/'


    try:
        r = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        html = r.text.lower()

        if "sorry, this page isn't available" in html:
            print(f"[-] Username not found: @{inp}")

        elif r.status_code == 200:
            print(f"[+] Username likely exists: {url}")

        else:
            print(f"[!] Status code: {r.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"[!] Error: {e}")

    

import exifread

def exif_extract():
    image_path = input('Enter image path to extract exif data: ')
    with open(image_path, 'rb') as f:
        tags = exifread.process_file(f)
        
        if not tags:
            print("No EXIF data found!")
            return

        for tag in tags.keys():
            print(f"{tag:25}: {tags[tag]}")


def base64_enc_dec():

    choice = input('You want to Encode a text or Decode? Enter choice(E/D): ')

    def dec():
        inp = input('Enter text to Decode: ')
        try:
            decoded = base64.b64decode(inp.encode('utf-8'))
            print('Decoded text: ', decoded.decode('utf-8') )
        
        except Exception as e:
            print(f'Failed to decode: {e}')

    
    def enc():
        inp = input('Enter text to Encode: ')
        try:
            encoded = base64.b64encode(inp.encode('utf-8'))
            print('Encoded text: ', encoded.decode('utf-8'))
        except Exception as e:
            print(f'Failed to encode text: {e}')




    

    if choice == 'E' or choice == 'Encode':
        enc()
    elif choice == 'D' or choice == 'Decode':
        dec()
    else:
        print('Ivalid choice!')



        

def password_strenght_check():

    inp = input('Enter password you want to check for strenght: ')

    if any(char in string.ascii_lowercase for char in inp) and any(char in string.digits for char in inp) and any(char in string.ascii_uppercase for char in inp) and any(char in string.punctuation for char in inp) and len(inp) > 8:

        print('✅ Strong password')
    else:
        print('❌ Password must be over 8 characters and must contain digits,upper letters, lower letters and special characters, You can use the password generator in Flex Tool')





def main():

    while True:

        print('''                                                                                
'########:'##:::::::'########:'##::::'##:
 ##.....:: ##::::::: ##.....::. ##::'##::
 ##::::::: ##::::::: ##::::::::. ##'##:::
 ######::: ##::::::: ######:::::. ###::::
 ##...:::: ##::::::: ##...:::::: ## ##:::
 ##::::::: ##::::::: ##:::::::: ##:. ##::
 ##::::::: ########: ########: ##:::. ##:
..::::::::........::........::..:::::..::
'########::'#######:::'#######::'##::::::::::'##::::'##:::::::'#######::
... ##..::'##.... ##:'##.... ##: ##:::::::::: ##:::: ##::::::'##.... ##:
::: ##:::: ##:::: ##: ##:::: ##: ##:::::::::: ##:::: ##::::::..::::: ##:
::: ##:::: ##:::: ##: ##:::: ##: ##:::::::::: ##:::: ##:::::::'#######::
::: ##:::: ##:::: ##: ##:::: ##: ##::::::::::. ##:: ##:::::::'##::::::::
::: ##:::: ##:::: ##: ##:::: ##: ##:::::::::::. ## ##:::'###: ##::::::::
::: ##::::. #######::. #######:: ########::::::. ###:::: ###: #########:
:::..::::::.......::::.......:::........::::::::...:::::...::.........::                                                                                           
    ''')
        
        print('-'*60)
        print('Made by glitch\nTikTok: https://tiktok.com/@glitch_blackhat\nWebsite: glitch-tools.netlify.app')
        print('-'*60)
        print("\nNETWORK TOOLS:")
        print(" [1]  Ping Scan            [2]  Port Scan")
        print(" [3]  DNS Lookup           [4]  Reverse DNS")
        print(" [5]  Dirb Scanner         [6]  IP Geolocation")
        print(" [7]  Whois Lookup         [8]  Subdomain Finder")
        print(" [9]  Rate Limit Tester    [10] Robots.txt Check")

        print("\nWEB / SECURITY TESTING:")
        print(" [11] Easy Fuzzing         [18] Google Dorks")

        print("\nCRYPTO / SECURITY:")
        print(" [12] MD5 Hash")
        print(" [13] SHA256 Hash")
        print(" [14] Password Generator")
        print(" [15] File Encrypt/Decrypt")

        print("\nRandom Shit:")
        print(" [16] Notes")
        print(" [17] Reverse Text")
        print(" [19] ASCII Art Generator")
        print(" [20] TikTok Username Check")
        print(" [21] Instagram Username search")
        print(' [22] Extract image exif data')
        print(" [23] base64 Docode/Encode")
        print(" [24] Password strenght checker")


        print('-'*60)
        print('')
        try:
            inp = int(input('Enter your choice(1-25): '))
        except ValueError:
            print('Please Enter the number of the Tool(1-25, 99 is exit)')
            return

        if inp == 1:
            os.system('cls' if os.name == 'nt' else 'clear')
            ping()
        elif inp == 2:
            os.system('cls' if os.name == 'nt' else 'clear')
            port_scanner()
        elif inp == 3:
            os.system('cls' if os.name == 'nt' else 'clear')
            dns()
        elif inp == 4:
            os.system('cls' if os.name == 'nt' else 'clear')
            reverse_dns()
        elif inp == 5:
            os.system('cls' if os.name == 'nt' else 'clear')
            dirb()
        elif inp == 6:
            os.system('cls' if os.name == 'nt' else 'clear')
            ip_geo()
        elif inp == 7:
            os.system('cls' if os.name == 'nt' else 'clear')
            whois_lookup()
        elif inp == 8:
            os.system('cls' if os.name == 'nt' else 'clear')
            subfinder()
        elif inp == 9:
            os.system('cls' if os.name == 'nt' else 'clear')
            rate_limit_tester()
        elif inp == 10:
            os.system('cls' if os.name == 'nt' else 'clear')
            search_robots()
        elif inp == 11:
            os.system('cls' if os.name == 'nt' else 'clear')
            simple_fuzzing()
        elif inp == 12:
            os.system('cls' if os.name == 'nt' else 'clear')
            md5_hash()
        elif inp == 13:
            os.system('cls' if os.name == 'nt' else 'clear')
            sha256()
        elif inp == 14:
            os.system('cls' if os.name == 'nt' else 'clear')
            passwd_gen()
        elif inp == 15:
            os.system('cls' if os.name == 'nt' else 'clear')
            file_encryption()
        elif inp == 16:
            os.system('cls' if os.name == 'nt' else 'clear')
            note()
        elif inp == 17:
            os.system('cls' if os.name == 'nt' else 'clear')
            reverse_text()
        elif inp == 18:
            os.system('cls' if os.name == 'nt' else 'clear')
            google_dorks()
        elif inp == 19:
            os.system('cls' if os.name == 'nt' else 'clear')
            ascii_art_gen()
        elif inp == 20:
            os.system('cls' if os.name == 'nt' else 'clear')
            tiktok_username_search()
        elif inp == 21:
            os.system('cls' if os.name == 'nt' else 'clear')
            insta_username_search()
        elif inp == 22:
            os.system('cls' if os.name == 'nt' else 'clear')
            exif_extract()
        elif inp == 23:
            os.system('cls' if os.name == 'nt' else 'clear')
            base64_enc_dec()
        elif inp == 24:
            os.system('cls' if os.name == 'nt' else 'clear')
            password_strenght_check()
        elif inp == 99:
            sys.exit()

        input('Press Enter to go back to Menu: ')
        os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == '__main__':
    show_website_tiktok()
    main()