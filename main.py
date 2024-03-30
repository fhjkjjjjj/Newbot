import random
import threading
import sqlite3
from telebot import *
import time
import json
import requests
import urllib.parse
json_file = open('config.json','r')
data = json.loads(json_file.read())
owner_id = data["owner_id"]
bot_a = data["bot"]
bot_api = bot_a
bot = telebot.TeleBot(bot_api)
stop_thread = False
def lvl_up(auth):
 data = {
  "operationName": "telegramGameSetNextBoss",
  "variables": {},
  "query": "mutation telegramGameSetNextBoss {\n  telegramGameSetNextBoss {\n    ...FragmentBossFightConfig\n    __typename\n  }\n}\n\nfragment FragmentBossFightConfig on TelegramGameConfigOutput {\n  _id\n  coinsAmount\n  currentEnergy\n  maxEnergy\n  weaponLevel\n  energyLimitLevel\n  energyRechargeLevel\n  tapBotLevel\n  currentBoss {\n    _id\n    level\n    currentHealth\n    maxHealth\n    __typename\n  }\n  freeBoosts {\n    _id\n    currentTurboAmount\n    maxTurboAmount\n    turboLastActivatedAt\n    turboAmountLastRechargeDate\n    currentRefillEnergyAmount\n    maxRefillEnergyAmount\n    refillEnergyLastActivatedAt\n    refillEnergyAmountLastRechargeDate\n    __typename\n  }\n  nonce\n  __typename\n}"
 }
 h = {
  "Host":"api-gw-tg.memefi.club",
  "authorization":f"Bearer {auth}",
  "user-agent":"Mozilla/5.0 (Linux; Android 7.1.2; Nexus 5 Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36",
  "content-type":"application/json",
  "x-requested-with":"org.telegram.messenger"
  }
 r = requests.post("https://api-gw-tg.memefi.club/graphql",headers=h,data=json.dumps(data))
 print(r.text)

def stop_background_task():
    global stop_thread
    stop_thread = True
def get_name(auth):
 data = {
  "operationName": "QueryTelegramUserMe",
  "variables": {},
  "query": "query QueryTelegramUserMe {\n  telegramUserMe {\n    firstName\n    lastName\n    telegramId\n    username\n    referralCode\n    _id\n    __typename\n  }\n}"
 }
 h = {
  "Host":"api-gw-tg.memefi.club",
  "authorization":f"Bearer {auth}",
  "user-agent":"Mozilla/5.0 (Linux; Android 7.1.2; Nexus 5 Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36",
  "content-type":"application/json",
  "x-requested-with":"org.telegram.messenger"
  }
 r = requests.post("https://api-gw-tg.memefi.club/graphql",headers=h,data=json.dumps(data))
 return json.loads(r.text)["data"]["telegramUserMe"]["firstName"]
def get_user_data(encoded_string):
 decoded_string = urllib.parse.unquote(encoded_string)
 key_value_pairs = decoded_string.split('&')
 data = {}
 for pair in key_value_pairs:
     key, value = pair.split('=')
     data[key] = urllib.parse.unquote(value)
 user_data = (urllib.parse.unquote(data['user']))
 user_data1 = json.loads(urllib.parse.unquote(data['user']))
 data["user_data"] = str(user_data)
 user_id = user_data1['id']
 username = user_data1['username']
 first_name = user_data1['first_name']
 last_name = user_data1['last_name']
 try:
  is_premium = user_data1['is_premium']
 except:
  is_premium = False
 data["user_id"] = user_id
 data["username"] = username
 data["first_name"] = first_name
 data["last_name"] = last_name
 data["is_premium"] = is_premium
 return data

def auth(url):
 j = (get_user_data(url))
 auth_date =j["auth_date"]
 hash = j["hash"]
 query_id = j["query_id"]
 user_id = j["user_id"]
 frist_name = j["first_name"]
 last_name = j["last_name"]
 user_name = j["username"]
 user = j["user"]
 is_premium = j["is_premium"]
 user_data = j["user_data"]
 checkDataString = 'auth_date='+str(auth_date)+'\nquery_id='+query_id+'\nuser='+user_data
 data = {
  "operationName": "MutationTelegramUserLogin",
  "variables": {
    "webAppData": {
      "auth_date": int(auth_date),
      "hash": hash,
      "query_id": query_id,
      "checkDataString": checkDataString,
      "user": {
        "id": int(user_id),
        "allows_write_to_pm": True,
        "first_name": frist_name,
        "last_name": last_name,
        "username": user_name,
        "language_code": "en"
      }
    }
  },
  "query": "mutation MutationTelegramUserLogin($webAppData: TelegramWebAppDataInput!) {\n  telegramUserLogin(webAppData: $webAppData) {\n    access_token\n    __typename\n  }\n}"
}
 dump = json.dumps(data)
 h = {
 "Host":"api-gw-tg.memefi.club",
 "user-agent":"Mozilla/5.0 (Linux; Android 7.1.2; Nexus 5 Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36",
 "content-type":"application/json",
 "x-requested-with":"org.telegram.messenger"
 }
 r = requests.post("https://api-gw-tg.memefi.club/graphql",data=dump,headers=h)
 if "User not found" in r.text:
  return "User not found"
 else:
  return json.loads(r.text)["data"]["telegramUserLogin"]["access_token"]


def get_coin(auth,name):
 json_file = open('config.json','r')
 data = json.loads(json_file.read())
 owner_id = data["owner_id"]
 global stop_thread
 nonce = "66079f143519d3f8280385"
 while not stop_thread:
  print(nonce)
  data = {
   "operationName": "MutationGameProcessTapsBatch",
   "variables": {
     "payload": {
       "nonce": nonce,
       "tapsCount": random.randint(15, 30)
     }
   },
   "query": "mutation MutationGameProcessTapsBatch($payload: TelegramGameTapsBatchInput!) {\n  telegramGameProcessTapsBatch(payload: $payload) {\n    ...FragmentBossFightConfig\n    __typename\n  }\n}\n\nfragment FragmentBossFightConfig on TelegramGameConfigOutput {\n  _id\n  coinsAmount\n  currentEnergy\n  maxEnergy\n  weaponLevel\n  energyLimitLevel\n  energyRechargeLevel\n  tapBotLevel\n  currentBoss {\n    _id\n    level\n    currentHealth\n    maxHealth\n    __typename\n  }\n  freeBoosts {\n    _id\n    currentTurboAmount\n    maxTurboAmount\n    turboLastActivatedAt\n    turboAmountLastRechargeDate\n    currentRefillEnergyAmount\n    maxRefillEnergyAmount\n    refillEnergyLastActivatedAt\n    refillEnergyAmountLastRechargeDate\n    __typename\n  }\n  nonce\n  __typename\n}"
  }
  h = {
  "Host":"api-gw-tg.memefi.club",
  "authorization":f"Bearer {auth}",
  "user-agent":"Mozilla/5.0 (Linux; Android 7.1.2; Nexus 5 Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36",
  "content-type":"application/json",
  "x-requested-with":"org.telegram.messenger"
  } 
  r = requests.post("https://api-gw-tg.memefi.club/graphql",headers=h,data=json.dumps(data))
  js =  json.loads(r.text)
  nonce = js["data"]["telegramGameProcessTapsBatch"]["nonce"]
  total_coin = js["data"]["telegramGameProcessTapsBatch"]["coinsAmount"]
  currentBoss = js["data"]["telegramGameProcessTapsBatch"]["currentBoss"]["level"]
  currentHealth = js["data"]["telegramGameProcessTapsBatch"]["currentBoss"]["currentHealth"]
  maxHealth = js["data"]["telegramGameProcessTapsBatch"]["currentBoss"]["maxHealth"]
  if int(currentHealth) == 0:
   lvl_up(auth)
  bot.send_message(chat_id=int(owner_id),parse_mode='HTML',text = (f"NAME -> {name}\nCOIN -> {total_coin}\nCURRENT BOSS -> {currentBoss}\nCURRENT BOSS HEALTH -> {currentHealth}\nBOSS MAX HEALTH -> {maxHealth}"))
  time.sleep(random.randint(5, 15))
@bot.message_handler(commands=['addnear'])
def addnear(message):
 conn = sqlite3.connect('new_data.db')
 cursor = conn.cursor()
 cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_data (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        data TEXT
    )
 ''')
 try:
  json_data = message.text.split("/addnear", 1)[1].strip()
  e = json_data
  user_id = message.from_user.id
  cursor.execute("INSERT INTO user_data (user_id, data) VALUES (?, ?)", (user_id, json_data))
  conn.commit()
  cursor.execute("SELECT user_id, GROUP_CONCAT(data, ',') FROM user_data WHERE user_id = ? GROUP BY user_id", (user_id,))
  user_data = cursor.fetchone()
  e = (user_data[1].split(","))
  bot.reply_to(message,parse_mode='HTML',text = (f"<b>DATA ADDED 😁</b>\n<b>TOTAL ID -> </b><i>{len(e)}😁</i>"))
 except:
  bot.reply_to(message,parse_mode='HTML',text = (f"<b>FAIL TO GET DATA UES -> </b><i>/addac (your data)</i>"))
@bot.message_handler(commands=['start_all'])
def near(message):
      json_file = open('config.json','r')
      data = json.loads(json_file.read())
      owner_id = data["owner_id"]
      while True:
        global stop_thread
        stop_thread = False
        conn = sqlite3.connect('new_data.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_data (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                data TEXT
            )
        ''')
        user_id = int(owner_id)
        cursor.execute("SELECT user_id, GROUP_CONCAT(data, ',') FROM user_data WHERE user_id = ? GROUP BY user_id", (user_id,))
        user_data = cursor.fetchone()
        accs = (user_data[1].split(","))
        sent_message = bot.send_message(chat_id=int(owner_id),parse_mode='HTML',text = (f"Starting ... 😁"))
        start_time = time.time()
        total_accs = len(accs)
        i=0
        total_farm = []
        for messag in accs:
         f = auth(messag)
         print(f)
         name = get_name(f)
         background_thread = threading.Thread(target=get_coin, args=(f,name,))
         background_thread.daemon = True
         background_thread.start()
        time.sleep(3600)
        stop_background_task()
#bot.infinity_polling()
print(lvl_up("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7Il9pZCI6IjY2MDZmMDkwZTYyZTE0ZjY1NmFiN2ZhOCIsInVzZXJuYW1lIjoiYW1hbm1vbmRhbDQ0NCJ9LCJzZXNzaW9uSWQiOiI2NjA4MjM0ZjlmNTc2OTYzNzAwZWJlYWEiLCJzdWIiOiI2NjA2ZjA5MGU2MmUxNGY2NTZhYjdmYTgiLCJpYXQiOjE3MTE4MDkzNTksImV4cCI6MTcxMjQxNDE1OX0.ASkqca46JkL5rWSInqEUMvVOD0yE8I2zWAEtElAQobc"))
