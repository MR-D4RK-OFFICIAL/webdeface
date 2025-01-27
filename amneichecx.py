import requests
from bs4 import BeautifulSoup
import json
import platform
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# আপনার Telegram Bot Token এখানে দিন
TOKEN = '7544036090:AAEmdii0YisVr9HwW6VSeS6HEevkVvUCpTs'  # এখানে আপনার বট টোকেন দিন

# ওয়েব স্ক্র্যাপিং ফাংশন
def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # এখানে আপনার প্রয়োজনীয় তথ্য সংগ্রহ করুন, যেমন <h1> ট্যাগ থেকে শিরোনাম
    title = soup.find('h1').text if soup.find('h1') else 'No Title Found'
    
    return title

# API থেকে তথ্য সংগ্রহের ফাংশন
def get_data_from_api(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        # এখানে আপনার প্রয়োজনীয় JSON ডেটা বের করুন
        return data
    else:
        return "Failed to fetch data from API."

# ফোনের কিছু তথ্য সংগ্রহ করার ফাংশন
def get_phone_info():
    ip_address = requests.get("https://api.ipify.org").text
    system_info = platform.system() + " " + platform.release()
    
    return {
        "IP Address": ip_address,
        "System Info": system_info
    }

# /start কমান্ড হ্যান্ডলার
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! Send /info to gather information.")

# /info কমান্ড হ্যান্ডলার
def info(update: Update, context: CallbackContext):
    # ফোনের তথ্য সংগ্রহ
    phone_info = get_phone_info()
    update.message.reply_text(f"Phone Info:\nIP Address: {phone_info['IP Address']}\nSystem Info: {phone_info['System Info']}")
    
    # ওয়েবসাইট স্ক্র্যাপ করা
    website_url = 'https://example.com'  # এখানে আপনার ওয়েবসাইট URL দিন
    title = scrape_website(website_url)
    update.message.reply_text(f"Website Title: {title}")
    
    # API থেকে তথ্য সংগ্রহ করা
    api_url = 'https://api.example.com/data'  # এখানে আপনার API URL দিন
    api_data = get_data_from_api(api_url)
    update.message.reply_text(f"API Data: {json.dumps(api_data, indent=4)}")

# Telegram Bot চালু করার ফাংশন
def main():
    # Telegram Bot চালু করা
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    # কমান্ড হ্যান্ডলার যোগ করা
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("info", info))

    # Bot শুরু করা
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()