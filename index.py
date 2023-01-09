import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials 

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
json = "./data/scrayping-spreadsheet.json"
credentials = ServiceAccountCredentials.from_json_keyfile_name(json, scope)
gc = gspread.authorize(credentials)

SPREADSHEET_KEY = "1V4HfR-AxJH_LnZ0pprkoh2_gBScC5AiTlVO2Drg0nqw"
worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1

search_query = worksheet.acell('B3').value


ua = UserAgent()
header = {"user-agent": ua.chrome} #botだとバレないようにheaderを設定
param = {"q": ["ボクシング", "全国"]}


url = 'https://ja.wikipedia.org/wiki/%E3%83%9C%E3%82%AF%E3%82%B7%E3%83%B3%E3%82%B0%E7%8F%BE%E7%8E%8B%E8%80%85%E4%B8%80%E8%A6%A7'
res = requests.get(url)
text = res.text
status = res.status_code
headers = res.headers


# ここからデータの抽出
soup = BeautifulSoup(text, "html.parser")
elms = soup.select('td[rowspan]:not([rowspan=""])')
for elm in elms:
    # print(elm.get_text(strip=True))
    print(elm.find('a'))

# elmsText = elms

