import pandas as pd
import requests as req
from bs4 import BeautifulSoup

pd.set_option('display.max_colwidth', 1000)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.1234.5678 Safari/537.36'
}
response = req.get('https://tgftp.nws.noaa.gov/logs/shipstats/', headers=headers, timeout=3)
soup = BeautifulSoup(response.text, 'html.parser')
if response.status_code == 200:
    links = soup.find_all('a')
    try:
        if links:
            newest = f'https://tgftp.nws.noaa.gov/logs/shipstats/{links[-1].get("href")}'
            response = req.get(newest, timeout=3)
            if response.status_code == 200:
                from io import StringIO
                data = StringIO(response.text)
                df = pd.read_csv(data)
                pd.options.display.max_rows = 9999
                pd.options.display.max_columns = 9999
                print(df)
                df.to_csv('shiplocs.csv', index=False)
                print('''

FULL RECOVERED DATA SAVED TO shiplocs.csv''')
            else:
                print(f'ERR: STATUS CODE {response.status_code}')
        else:
            print('nvm I hacked it but I could find anything')
    except req.exceptions.RequestException as e:
        print(f"Error: {e}")
elif response.status_code == 404:
    print('Oh dang I was trying to hack something i though existed but it doesnt anymore lol.')
else:
    print(f'Uhh... I was trying to hack them but I got a status code {response.status_code}')
