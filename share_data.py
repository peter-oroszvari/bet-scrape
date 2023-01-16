import requests
import json
import pandas as pd
import io
from requests.utils import dict_from_cookiejar
from bs4 import BeautifulSoup

response = requests.get('https://bet.hu/oldalak/adatletoltes')
# Extracting JSESSIONID
cookie = dict_from_cookiejar(response.cookies)

# Extracting the csrf-token value from the HTML response
soup = BeautifulSoup(response.text, 'html.parser')
meta_tag = soup.find('meta', attrs={'name': '_csrf'})
csrf_token = meta_tag['content']

# preparing the Cookie value for the POST request header
jes = 'JSESSIONID='+ cookie['JSESSIONID'] +'; cookiesAcceptWarning=null'

# Adding csrf-token to the URL of the POST request
url = "https://www.bet.hu/oldalak/adatletoltes/$rspid0x117390x12/$rihistoricalGenerator?_csrf=" + csrf_token

# Payload of the POST request

payload = json.dumps({
  "startingValue": "2022.05.16.",
  "endingValue": "2023.01.14.",
  "resolution": "DAY_TO_DAY",
  "market": "PROMPT",
  "format": "CSV",
  "type": "OHLC",
  "currentCategory": "W_RESZVENYA",
  "selectionList": [
    {
      "category": "Részvények Prémium",
      "selectedInstruments": [
        {
          "id": "528",
          "code": "OTP"
        }
      ]
    }
  ]
})

# Header of the POST request

headers = {
  'Accept': '*/*',
  'Accept-Language': 'hu-HU,hu;q=0.9,en-US;q=0.8,en;q=0.7',
  'Connection': 'keep-alive',
  'Content-type': 'application/json',
  'Cookie': jes,
  'Origin': 'https://www.bet.hu',
  'Referer': 'https://www.bet.hu/',
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}

# Sending the post request

response = requests.request("POST", url, headers=headers, data=payload)

# Displaying the result of the POST request

if response.status_code == 200:
    csv_string = response.content.decode('utf-8')
    csv_file = io.StringIO(csv_string)
    df = pd.read_csv(csv_file)
    data = df.to_dict("records")
    print(data)

else:
    print("Request failed with status code: {}".format(response.status_code))