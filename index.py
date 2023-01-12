import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import re #正規表現
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
json = "./data/scrayping-spreadsheet.json"
credentials = ServiceAccountCredentials.from_json_keyfile_name(json, scope)
gc = gspread.authorize(credentials)

SPREADSHEET_KEY = "1V4HfR-AxJH_LnZ0pprkoh2_gBScC5AiTlVO2Drg0nqw" #dとeditの間
worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1

search_query = worksheet.acell('C3').value


ua = UserAgent()
header = {"user-agent": ua.chrome} #botだとバレないようにheaderを設定
param = {"q": ["ボクシング", "全国"]}


searchUrl = worksheet.acell('B3').value
res = requests.get(searchUrl)
text = res.text #テキストで取得する


# ここからデータの抽出
soup = BeautifulSoup(text, "html.parser")
elms = soup.select('.wikitable td')
result = [["name", "record", "country", "throne"]]
for elm in elms:
    throne = elm.select_one('b')
    throne = throne.text if (throne) else "none"

    country = elm.select_one("a:first-of-type")
    res = re.match("の旗", country)
    if (res):
        print("マッチしました")
    country = country["title"] if (country) else "none"

    name = elm.select_one('a:last-of-type')
    name = name.text if (name) else "none"

    record = elm.get_text(strip=True)
    record = record[-13:] if (record) else "none" #最後からのテキストを抜き出す

    result.append([name, record, country, throne])
print(result[1:3])