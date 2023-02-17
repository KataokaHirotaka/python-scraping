import requests
from bs4 import BeautifulSoup
import gspread
from gspread.exceptions import *
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import sys

url = "https://turu-turu.net/searcheventarea2/" #全国のボクシングジムの一覧
res = requests.get(url)
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
json = "python-scrayping-377806.json"
credentials = ServiceAccountCredentials.from_json_keyfile_name(json, scope)
gc = gspread.authorize(credentials)


SPREADSHEET_KEY = "1dH67QKH-nONoJtG6YrDyi1ddGUs-9Gu3r4C1FQe7UDs" #dとeditの間
worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1




#書き込み用の文字列を作成
items = ['Hello', 'World']
# シートへ文字列を追加
worksheet.append_row(items)

soup = BeautifulSoup(res.text, "html.parser")

elms = soup.select("#list_contents2")

gym_name_array = []
gym_url_array = []
print_code_array = []
address_array = []
phone_num_array = []
access_array = []
affiliation_array = []

for elm in elms:
    gym_name_array.append(elm.select_one("h3 > a").text)
    gym_url_array.append(elm.select_one("h3 > a").get("href"))
    list_box2_right = elm.select_one(".list_box2_right")
    print_code_array.append(list_box2_right.select_one("p:first-child").text)
    address_array.append(list_box2_right.select_one('p:nth-child(2)').text)
    phone_num_array.append(list_box2_right.select_one("p:nth-child(3) > a").text)
    access_array.append(list_box2_right.select_one("p:nth-child(4)").text)
    # affiliation_array.append(list_box2_right.select_one("p:nth-child(6)").text)

print(gym_url_array)
