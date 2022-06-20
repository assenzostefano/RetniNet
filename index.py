import psutil
import requests
import random
import pyfiglet
import socket
import threading
import datetime
import telebot
import time
import ast
import ffmpeg
import os
import python_weather
import asyncio
import json
import goslate
import urllib.request
import urllib.parse
import logging
import deepl
from dotenv import load_dotenv
from yt_dlp import YoutubeDL
from platform import system
from tqdm.auto import tqdm
from importlib.metadata import files
from dataclasses import dataclass
from jmespath import search
from telebot import types, telebot
from pytube import YouTube
from bs4 import BeautifulSoup
from gc import callbacks

load_dotenv()
API_TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(API_TOKEN)
print("Il bot si è avviato con successo!")


#Command /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    print("Triggered command START.")
    bot.send_photo(chat_id, photo='https://i.imgur.com/6YPJBze.png')
    messageText = "✋ Benvenuto su <b>RetniNet!</b>\n\n<b>RetniNet</b> è un bot privato per <b>automatizzare</b> e <b>semplificare</b> cose che facciamo quotidianamente. \n\n👨‍💻 Creato & sviluppato da @Stef58_Official"
    bot.send_message(chat_id,messageText, parse_mode="HTML")

#Command /music
@bot.message_handler(commands=['music'])
def select_music(pm):
    print("Triggered command MUSIC.")
    sent_msg = bot.send_message(pm.chat.id, "Inserisci il link della canzone:")
    bot.register_next_step_handler(sent_msg, music_step)
    

def music_step(pm):
    if pm.text.startswith('https://www.youtube.com/') or pm.text.startswith('https://youtu.be/'):
        ytdl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
        }],
    }
        with YoutubeDL(ytdl_opts) as ydl:
            url = pm.text
            info = ydl.extract_info(url, download=False)
            name = info.get('title')
            id = info.get('id')
            ydl.download([id])
            send_message = "🎶 La canzone <b>" + name + "</b> è stata scaricata con successo!"
            bot.send_message(pm.chat.id, send_message, parse_mode="HTML")
            bot.send_audio(pm.chat.id, audio=open(name + '.mp3', 'rb'))
    else:
        bot.send_message(pm.chat.id, "🚫 Devi inserire un <b>link</b> valido!")

#Command /meteo
@bot.message_handler(commands=['meteo'])
def meteo(pm):
    print("Triggered command METEO.")
    sent_msg = bot.send_message(pm.chat.id, "🏙️ Inserisci la città:")
    bot.register_next_step_handler(sent_msg, meteo_step)

def meteo_step(message):
    translator = deepl.Translator(os.getenv('DEEPL_TOKEN'))
    result = translator.translate_text('hi', target_lang='IT') 
    translated_text = result.text
    city = message.text
    token_weather = os.environ.get('WEATHER_TOKEN')
    response = requests.get("https://api.openweathermap.org/data/2.5/weather?q="+city+",it&APPID="+token_weather).json()
    weather = response['weather'][0]['main'] #
    temp = response['main']['temp']
    temp = temp - 273.15
    weather_translate = translator.translate_text(weather, target_lang='IT')
    result_weather = weather_translate.text
    bot.send_message(message.chat.id, "🌡️ La temperatura in " + city + " è di " + str(temp) + "°C")
    bot.send_message(message.chat.id, "🌧️ La condizione è " + result_weather)

#Command /stats
@bot.message_handler(commands=['stats'])
def uptime(message):
    print("Triggered command STATS.")
    cpuUsage = psutil.cpu_percent(interval=1)
    ramTotal = int(psutil.virtual_memory().total/(1024*1024)) #GB
    ramUsage = int(psutil.virtual_memory().used/(1024*1024)) #GB
    ramFree = int(psutil.virtual_memory().free/(1024*1024)) #GB
    ramUsagePercent = psutil.virtual_memory().percent
    msg = '''
CPU & RAM Info

🟩 Utilizzo CPU = {} %
RAM
Totale = {} MB
Usato = {} MB
Libero  = {} MB
In uso = {} %\n'''.format(cpuUsage,ramTotal,ramUsage,ramFree,ramUsagePercent)
    bot.send_message(message.chat.id,msg)

#Command /pastebin
@bot.message_handler(commands=['pastebin'])
def pastebin(message):
    print("Triggered command PASTEBIN.")
    sent_msg = bot.send_message(message.chat.id, "📋 Inserisci il testo:")
    bot.register_next_step_handler(sent_msg, pastebin_step)

def pastebin_step(message):
    chat = message.chat.id
    text = message.text
    site = 'https://pastebin.com/api/api_post.php'
    dev_key = os.environ.get('PASTEBIN_TOKEN')
    code = text     
    our_data = urllib.parse.urlencode({"api_dev_key": dev_key, "api_option": "paste", "api_paste_code": code})  
    our_data = our_data.encode()                    
    resp = urllib.request.urlopen(site, our_data)
    resp = resp.read()
    send_msg = "📋 Il tuo <b>codice</b> è stato inviato con successo!\n\n<b>Link:</b> " + str(resp)
    bot.send_message(chat,send_msg, parse_mode="HTML")

#Command /epicgames

@bot.message_handler(commands=['epicgames'])
def epicgames(message):
    text = message.text
    bot.send_message(message.chat.id, "🎮 Vuoi vedere il gioco disponibile al momento o quello futuro? (disponibile/futuro)")
    bot.register_next_step_handler(message, epicgames_step)

def epicgames_step(message):
    text = message.text
    if text == 'disponibile':
        print("Triggered command EPICGAMES DISPONIBILE.")
        #URL API
        url = "https://api.plenusbot.xyz/epic_games?country=IT"
        response = requests.get(url).json()
        #Title of current games
        current_games = response['currentGames'][0]['title']
        #Image current games
        image_currentgames = response['currentGames'][0]['keyImages'][0]['url']
        #Description current games
        current_games_description = response['currentGames'][0]['description']
        #Token for translate
        translator = deepl.Translator(os.getenv('DEEPL_TOKEN'))
        #Translate description current games
        description_translate = translator.translate_text(current_games_description, target_lang='IT')
        result_description = description_translate.text
        send_img = bot.send_photo(message.chat.id, image_currentgames)
        sent_msg = bot.send_message(message.chat.id, "🎮 Il gioco gratis di oggi è " + current_games + "\n\n" + result_description)
    else:
        print("Triggered command EPICGAMES FUTURO.")
        #URL API
        url = "https://api.plenusbot.xyz/epic_games?country=IT"
        response = requests.get(url).json()
        #Title of future games
        future_games1 = response['nextGames'][0]['title']
        #Image future games
        image_futuregames1 = response['nextGames'][0]['keyImages'][0]['url']
        #Description future games
        future_games_description1 = response['nextGames'][0]['description']
        #Token for translate
        translator = deepl.Translator(os.getenv('DEEPL_TOKEN'))
        description_translate1 = translator.translate_text(future_games_description1, target_lang='IT')
        result_description1 = description_translate1.text
        send_img = bot.send_photo(message.chat.id, image_futuregames1)
        sent_msg = bot.send_message(message.chat.id, "🎮 Il gioco futuro è " + future_games1 + "\n\n" + result_description1)
        #Title of future games
        future_games2 = response['nextGames'][1]['title']
        #Image future games
        image_futuregames2 = response['nextGames'][1]['keyImages'][0]['url']
        #Description future games
        future_games_description2 = response['nextGames'][1]['description']
        #Traslate description future games
        description_translate2 = translator.translate_text(future_games_description2, target_lang='IT')
        result_description2 = description_translate2.text
        send_img = bot.send_photo(message.chat.id, image_futuregames2)
        sent_msg = bot.send_message(message.chat.id, "🎮 Il gioco futuro è " + future_games2 + "\n\n" + result_description2)

bot.polling()