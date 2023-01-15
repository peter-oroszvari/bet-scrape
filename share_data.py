import requests
import json
import pandas as pd
import io


url = "https://www.bet.hu/oldalak/adatletoltes/$rspid0x117390x12/$rihistoricalGenerator?_csrf=3b13429f-c797-42bf-a72b-00fb33d108da"

payload = json.dumps({
  "startingValue": "2022.12.16.",
  "endingValue": "2023.01.14.",
  "resolution": "DAY_TO_DAY",
  "market": "PROMPT",
  "format": "CSV",
  "type": "DETAILED",
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
headers = {
  'Accept': '*/*',
  'Accept-Language': 'hu-HU,hu;q=0.9,en-US;q=0.8,en;q=0.7',
  'Connection': 'keep-alive',
  'Content-type': 'application/json',
  'Cookie': '_ga=GA1.2.331254811.1673780113; _gid=GA1.2.1995785858.1673780113; _fbp=fb.1.1673780112827.910819643; cookiesAcceptWarning=null; JSESSIONID=1816506C3D22CDC2AD34AA9A15838F62',
  'Origin': 'https://www.bet.hu',
  'Referer': 'https://www.bet.hu/',
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}

response = requests.request("POST", url, headers=headers, data=payload)

if response.status_code == 200:
    csv_string = response.content.decode('utf-8')
    csv_file = io.StringIO(csv_string)
    df = pd.read_csv(csv_file)
    data = df.to_dict("records")

else:
    print("Request failed with status code: {}".format(response.status_code))
    

print(data)

