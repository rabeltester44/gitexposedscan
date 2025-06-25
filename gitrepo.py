import requests
from bs4 import BeautifulSoup
import concurrent.futures

# Color codes for terminal output
VERMELHO = "\033[1;31m"
VERDE = "\033[92m"
BRANCO = "\033[0;0m"
AMARELO = "\033[1;93m"
CLARO = "\033[93m"

print(f'{VERMELHO}[ MASS GIT SCANNER ]')

hosts = input(CLARO + 'Input List: ' + BRANCO)

try:
    # Read file line-by-line to avoid memory issues
    with open(hosts, 'r', encoding="utf8") as file:
        sites = file.readlines()
except FileNotFoundError as e:
    print('\n', hosts, 'list not found')
    exit()

content_git = 'ref: refs/heads/master'
header = {'User-Agent':
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0'
          }

def git_scan(site):
    site = site.strip()
    try:
        git = requests.get(f'http://{site}/.git/HEAD', headers=header, timeout=10)
        response_git = git.text
        if content_git in response_git:
            with open('gitfound.txt', 'a') as result_file:
                result_file.write(f'http://{site}/.git/\n')
            print(f'http://{site}', VERDE + '[+] Git found ! [+]' + BRANCO)
        else:
            print(f'http://{site}', VERMELHO + '[-] Git not found ! [-]' + BRANCO)
    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout, requests.exceptions.TooManyRedirects, requests.exceptions.InvalidSchema, requests.exceptions.InvalidURL) as e:
        print(f'http://{site}', AMARELO + '[-] Invalid url or site down [-]' + BRANCO)

try:
    num_threads = int(input("Enter the number of threads to use: "))
except ValueError:
    print("Invalid number of threads. Exiting.")
    exit()

with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    futures = [executor.submit(git_scan, site) for site in sites]

# Wait for all threads to finish
concurrent.futures.wait(futures)

print("Scanning complete. Results saved in 'gitfound.txt'")
