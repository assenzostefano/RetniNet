import psutil
import random
import pyfiglet
import socket
import threading
import datetime
import subprocess
import telebot
import time
import ast
import ffmpeg
import os
import requests
import python_weather
import asyncio
import requests
import json
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

API_TOKEN = '5407819601:AAEfiaw8ZNlyBHftLsJR5VAcMyv257tWHMY'

bot = telebot.TeleBot(API_TOKEN)
print("Il bot si è avviato con successo!")


#Command /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    print("Triggered command START.")
    #bot.send_photo(message.chat.id, photo='https://i.imgur.com/XqQZQ.jpg')
    bot.reply_to(message, "😊 Benvenuto su **RetniNet**" "\n \nRetniNet è un bot privato per automatizzare e semplificare cose che facciamo quotidianamente. \n \n Creato & sviluppato da @Stef58_Official")

#Command /music
@bot.message_handler(commands=['music'])
def select_music(pm):
    print("Triggered command MUSIC.")
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
        }],
    }
    sent_msg = bot.send_message(pm.chat.id, "Inserisci il link della canzone:")
    bot.register_next_step_handler(sent_msg, music_step)
    bot.send_message(pm.chat.id, "🎶 Stiamo scaricando la canzone attenda...")

def music_step(message):
    ytdl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'song.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    url = message.text
    video = url
    with YoutubeDL(ytdl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        name = info.get('title')
        id = info.get('id')
        ydl.download([id])
        bot.send_message(message.chat.id, "🎶" + name + " è stata scaricata con successo!")
        send_music(message)

def send_music(message):
    bot.send_audio(message.chat.id, audio=open('song.mp3', 'rb'))
    os.remove('song.mp3')
        
#Command /meteo
@bot.message_handler(commands=['meteo'])
def meteo(pm):
    print("Triggered command METEO.")
    sent_msg = bot.send_message(pm.chat.id, "Inserisci la città:")
    bot.register_next_step_handler(sent_msg, meteo_step)

def meteo_step(message):
    city = message.text
    response = requests.get("https://api.openweathermap.org/data/2.5/weather?q="+city+",it&APPID=dd9c01763daea0b5539db05fbfbe4cb6").json()
    weather = response['weather'][0]['main']
    temp = response['main']['temp']
    temp = temp - 273.15
    bot.send_message(message.chat.id, "🌡️ La temperatura in " + city + " è di " + str(temp) + "°C")
    bot.send_message(message.chat.id, "🌧️ La condizione è " + weather)

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

Utilizzo CPU = {} %
RAM
Totale = {} MB
Usato = {} MB
Libero  = {} MB
In uso = {} %\n'''.format(cpuUsage,ramTotal,ramUsage,ramFree,ramUsagePercent)
    bot.send_message(message.chat.id,msg)

bot.polling()