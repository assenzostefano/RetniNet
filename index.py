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
import logging
import deepl
import spotipy
import pyshorteners
import pdf2docx
import PyPDF2
import urllib
from currency_converter import CurrencyConverter
from googletrans import Translator
from random import randint
from random import random
from fileinput import filename
from pdf2docx import Converter, parse
from spotipy.oauth2 import SpotifyClientCredentials
from youtube_search import YoutubeSearch
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
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

load_dotenv()
API_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

#Start bot
logging.info("Il bot si è avviato con successo!")


#Command /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    logging.info("Triggered command START.")
    bot.send_photo(chat_id, photo='https://i.imgur.com/6YPJBze.png')
    messageText = "✋ Benvenuto su <b>RetniNet!</b>\n\n<b>RetniNet</b> è un bot privato per <b>automatizzare</b> e <b>semplificare</b> cose che facciamo quotidianamente. \n\n👨‍💻 Creato & sviluppato da @Stef58_Official"
    bot.send_message(chat_id, messageText, parse_mode="HTML")

#Command /music


@bot.message_handler(commands=['music'])
def select_music(pm):
    logging.info("Triggered command MUSIC.")
    sent_msg = bot.send_message(pm.chat.id, "Inserisci il link della canzone:")
    bot.register_next_step_handler(sent_msg, music_step)


def music_step(pm):
    text = pm.text
    #Check if the link is correct (Youtube and Spotify links only)
    if text.startswith('https://www.youtube.com/') or text.startswith('https://youtu.be/'):
        ytdl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'music_cache/%(title)s.%(ext)s',
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
            send_message = "🎶 La canzone <b>" + name + \
                    "</b> è stata scaricata con successo!"
            bot.send_message(pm.chat.id, send_message, parse_mode="HTML")
            bot.send_audio(pm.chat.id, audio=open("music_cache/" + name + '.mp3', 'rb'))
            os.remove("music_cache/" + name + '.mp3')
    #If the link for spotify ends with /album, /user, /playlist ecc.. send a error message
    elif pm.text.startswith('https://open.spotify.com/track/'):
        ytdl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'music_cache/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with YoutubeDL(ytdl_opts) as ydl:
            message = pm.text
            sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.getenv('SPOTIFY_ID'), client_secret=os.getenv('SPOTIFY_SECRET')))
            track = sp.track(message)
            name = track["name"]
            artist = track["artists"][0]["name"]
            results = YoutubeSearch(artist + " - " + name, max_results=1).to_json()
            get_link = json.loads(results)
            link = get_link['videos'][0]['url_suffix']
            print_link = 'https://youtube.com' + link
            url = print_link
            info = ydl.extract_info(url, download=False)
            name = info.get('title')
            id = info.get('id')
            ydl.download([id])
            send_message = "🎶 La canzone <b>" + name + \
                "</b> è stata scaricata con successo!"
            bot.send_message(pm.chat.id, send_message, parse_mode="HTML")
            bot.send_audio(pm.chat.id, audio=open("music_cache/" + name + '.mp3', 'rb'))
            os.remove("music_cache/" + name + '.mp3')
            logging.info("\"" + name + "\" è stato scaricato ed eliminato con successo!")

    elif pm.text.startswith('https://youtube.com/') or pm.text.startswith('youtube.com/'):
        bot.send_message(
            pm.chat.id, "🚫 <b>Errore</b>\n\n<b>Il link</b> inserito non è valido!")
    else:
        try:
            with YoutubeDL(ytdl_opts) as ydl:
                url = pm.text
                info = ydl.extract_info(url, download=False)
                name = info.get('title')
                id = info.get('id')
                ydl.download([id])
                send_message = "🎶 La canzone <b>" + name + \
                    "</b> è stata scaricata con successo!"
                bot.send_message(pm.chat.id, send_message, parse_mode="HTML")
                bot.send_audio(pm.chat.id, audio=open("music_cache/" + name + '.mp3', 'rb'))
                os.remove("music_cache/" + name + '.mp3')
        except:
            chat = pm.chat.id
            send_msg = "🚫 Errore!\n\n<b>Errore:</b> <i>Impossibile scaricare la canzone</i>"
            bot.send_message(chat, send_msg, parse_mode="HTML")

        else:
            chat = pm.chat.id
            bot.send_message(chat, pm.chat.id,"🚫 Devi inserire un <b>link</b> valido!")


#Command /meteo
@bot.message_handler(commands=['meteo'])
def meteo(pm):
    logging.info("Triggered command METEO.")
    sent_msg = bot.send_message(pm.chat.id, "🏙️ Inserisci la città:")
    bot.register_next_step_handler(sent_msg, meteo_step)


def meteo_step(message):
    translator = deepl.Translator(os.getenv('DEEPL_TOKEN'))
    result = translator.translate_text('hi', target_lang='IT')
    translated_text = result.text
    city = message.text
    token_weather = os.environ.get('WEATHER_TOKEN')
    response = requests.get("https://api.openweathermap.org/data/2.5/weather?q="+city+",it&APPID="+token_weather).json()
    weather = response['weather'][0]['main']
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
    ramTotal = int(psutil.virtual_memory().total/(1024*1024))  # GB
    ramUsage = int(psutil.virtual_memory().used/(1024*1024))  # GB
    ramFree = int(psutil.virtual_memory().free/(1024*1024))  # GB
    ramUsagePercent = psutil.virtual_memory().percent
    msg = '''
CPU & RAM Info

🟩 Utilizzo CPU = {} %
RAM
Totale = {} MB
Usato = {} MB
Libero  = {} MB
In uso = {} %\n'''.format(cpuUsage, ramTotal, ramUsage, ramFree, ramUsagePercent)
    bot.send_message(message.chat.id, msg)

#Command /pastebin


@bot.message_handler(commands=['pastebin'])
def pastebin(message):
    logging.info("Triggered command PASTEBIN.")
    sent_msg = bot.send_message(message.chat.id, "📋 Inserisci il testo:")
    bot.register_next_step_handler(sent_msg, pastebin_step)


def pastebin_step(message):
    chat = message.chat.id
    text = message.text
    site = 'https://pastebin.com/api/api_post.php'
    dev_key = os.environ.get('PASTEBIN_TOKEN')
    code = text
    our_data = urllib.parse.urlencode(
        {"api_dev_key": dev_key, "api_option": "paste", "api_paste_code": code})
    our_data = our_data.encode()
    resp = urllib.request.urlopen(site, our_data)
    resp = resp.read()
    send_msg = "📋 Il tuo <b>codice</b> è stato inviato con successo!\n\n<b>Link:</b> " + \
        str(resp)
    bot.send_message(chat, send_msg, parse_mode="HTML")

#Command /epicgames


@bot.message_handler(commands=['epicgames'])
def epicgames(message):
    text = message.text
    bot.send_message(
        message.chat.id, "🎮 Vuoi vedere il gioco disponibile al momento o quello futuro? (disponibile/futuro)")
    bot.register_next_step_handler(message, epicgames_step)


def epicgames_step(message):
    text = message.text
    if text == 'disponibile' or text == 'Disponibile':
        logging.info("Triggered command EPICGAMES DISPONIBILE.")
        # URL API
        url = "https://api.plenusbot.xyz/epic_games?country=IT"
        response = requests.get(url).json()
        # Title of current games
        current_games = response['currentGames'][0]['title']
        # Image current games
        image_currentgames = response['currentGames'][0]['keyImages'][0]['url']
        # Description current games
        current_games_description = response['currentGames'][0]['description']
        # Token for translate
        translator = deepl.Translator(os.getenv('DEEPL_TOKEN'))
        # Translate description current games
        description_translate = translator.translate_text(
            current_games_description, target_lang='IT')
        result_description = description_translate.text
        send_img = bot.send_photo(message.chat.id, image_currentgames)
        sent_msg = bot.send_message(message.chat.id, "🎮 Il gioco gratis di oggi è " + current_games + "\n\n" + result_description)
    else:
        logging.info("Triggered command EPICGAMES FUTURO.")
        # URL API
        url = "https://api.plenusbot.xyz/epic_games?country=IT"
        response = requests.get(url).json()
        # Title of future games
        future_games1 = response['nextGames'][0]['title']
        # Image future games
        image_futuregames1 = response['nextGames'][0]['keyImages'][0]['url']
        # Description future games
        future_games_description1 = response['nextGames'][0]['description']
        # Token for translate
        translator = deepl.Translator(os.getenv('DEEPL_TOKEN'))
        description_translate1 = translator.translate_text(future_games_description1, target_lang='IT')
        result_description1 = description_translate1.text
        send_img = bot.send_photo(message.chat.id, image_futuregames1)
        sent_msg = bot.send_message(message.chat.id, "🎮 Il gioco futuro è " + future_games1 + "\n\n" + result_description1)
        # Title of future games
        future_games2 = response['nextGames'][1]['title']
        # Image future games
        image_futuregames2 = response['nextGames'][1]['keyImages'][0]['url']
        # Description future games
        future_games_description2 = response['nextGames'][1]['description']
        # Traslate description future games
        description_translate2 = translator.translate_text(future_games_description2, target_lang='IT')
        result_description2 = description_translate2.text
        send_img = bot.send_photo(message.chat.id, image_futuregames2)
        sent_msg = bot.send_message(message.chat.id, "🎮 Il gioco futuro è " + future_games2 + "\n\n" + result_description2)

#Command /shutdown
@bot.message_handler(commands=['shutdown'])
def shutdown(message):
    logging.ingo("Triggered SHUTDOWN")
    text = message.text
    sent_msg = bot.send_message(message.chat.id, "Sei sicuro di voler spegnere il pc?")
    bot.register_next_step_handler(sent_msg, shutdown_step)

def shutdown_step(message):
    id = message.from_user.id
    text = message.text
    id_owner = os.getenv('USER_ID')
    if id == 771375637:

        if text == "si" or text == "Si" or text == "y" or text == "Y" or text == "Yes" or text == "yes":
            bot.send_message(message.chat.id, "Il computer è stato spento con successo!")
            logging.info("Triggered Shutdown")
            url = os.getenv("PASSWORD")
            requests.get(url)
        else:
            bot.send_message(message.chat.id, "⚠️ Hai annullato l'operazione!")

#Command /shortlink

@bot.message_handler(commands=['shortlink'])
def shortlink(message):
    logging.info("Triggered SHORTLINK")
    text = message.text
    sent_msg = bot.send_message(message.chat.id, "Inserisci il link:")
    bot.register_next_step_handler(sent_msg, shortlink_step)

def shortlink_step(message):
    text = message.text
    type_tiny = pyshorteners.Shortener()
    short_url = type_tiny.tinyurl.short(text)
    bot.send_message(message.chat.id, "Ecco a te lo shortlink: " + short_url)

#Command /uptime
@bot.message_handler(commands=['uptime'])
def uptime(message):
    logging.info("Triggered UPTIME")
    sent_msg = bot.send_message(message.chat.id, "Manda il link del sito che vuoi controllare.")
    bot.register_next_step_handler(sent_msg, uptime_step)

def uptime_step(message):
    text = message.text
    try:
        x = requests.get(text)
        if x.status_code == 200:
            bot.send_message(message.chat.id, "Il sito è online, puoi festeggiare adesso! :tada:")
    except requests.exceptions.ConnectionError:
        bot.send_message(message.chat.id, "Il sito non esiste oppure è offline, sad...")
    # status_code = urllib.request.urlopen(url).getcode()
    # website_is_up = status_code == 200
    # try
    #     if website_is_up == True:
    #         bot.send_message(message.chat.id, "Il sito è online!")
    # except:
    #     bot.send_message(message.chat.id, "Si è verificato un errore")

#Command /convert
@bot.message_handler(commands=["convertpdf"])
def addfile(message):
    logging.info("Triggered CONVERT")
    sent_msg = bot.send_message(message.chat.id, "Manda il file pdf che vuoi convertire in docx")
    bot.register_next_step_handler(sent_msg, convert)

def convert(message):
    file_name = message.document.file_name
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    docx_file = file_name + '.docx'
    pdf_file = file_name
    cv = Converter(pdf_file)
    cv.convert(docx_file)
    cv.close()
    html_doc = open(docx_file, 'rb')
    sent_msg = bot.send_message(message.chat.id, "Il file è stato convertito con successo!")
    bot.send_document(message.chat.id, html_doc)
    os.remove(pdf_file)

#Command /cloud
@bot.message_handler(commands=["cloud"])
def cloud(message):
    logging.info("Triggered CLOUD")
    sent_msg = bot.send_message(message.chat.id, "Invia il file che vuoi caricare")
    bot.register_next_step_handler(sent_msg, cloud_step)

def cloud_step(message):
    id = message.from_user.id
    file_name = message.document.file_name
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    if file_name == file_name:
        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)
        value = randint(1, 9999)
        old_name = file_name
        new_name = str(value) + file_name
        os.rename(old_name, new_name)
        os.replace(new_name, 'storage/'+new_name)
    else:
        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)
        os.replace(file_name, 'storage/'+file_name)
    bot.send_message(message.chat.id, "Il tuo file è stato caricato con successo! Ecco l'id del tuo file "+new_name)
    bot.send_message(message.chat.id, "Se vuoi scaricare il file fai /cloud download + l'id del file")
    dic_exm ={

    "filename" : new_name,
    "user_id" : id,

    }
    with open('data.json', 'a') as f:
        json.dump(dic_exm, f, indent=2)
        f.write('\n')

@bot.message_handler(commands=["translatepdf"])
def translatepdf(message):
    logging.info("Triggered TRANSLATE PDF")
    sent_msg = bot.send_message(message.chat.id, "Scrivi il messaggio che vuoi tradurre.")
    bot.register_next_step_handler(sent_msg, translatepdf_step)

def translatepdf_step(message):
    id = message.from_user.id
    file_name = message.document.file_name
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    input_file = file_name
    text_file = file_name + '.txt'
    os.replace(input_file, 'storage/'+input_file)
    input_file_position = 'storage/'+input_file
    with open(input_file_position, "rb") as pdf_file:
        read_pdf = PyPDF2.PdfFileReader(pdf_file)
        number_of_pages = read_pdf.getNumPages()
        page = read_pdf.pages[0]
        page_content = page.extractText()
    with open(text_file, 'w') as f:
        f.write(page_content)
    os.replace(text_file, 'storage/'+text_file)
    text_file_position = 'storage/'+text_file
    f = open(text_file_position)
    contents = f.read()
    translator = Translator()
    translated_text = translator.translate(contents, dest='it')
    bot.send_message(message.chat.id, translated_text.text)
    os.remove(input_file_position)
    os.remove(text_file_position)

#Command /convertmoney
@bot.message_handler(commands=["convertmoney"])
def convertmoney(message):
    logging.info("Triggered CONVERT MONEY")
    text = message.text
    sent_msg = bot.send_message(message.chat.id, "In che valuta vuoi convertire?")
    bot.register_next_step_handler(sent_msg, convertmoney_step)


def convertmoney_step(message):
    text = message.text
    c = CurrencyConverter()
    second = text
    sent_msg = bot.send_message(message.chat.id, "Inserisci quanto vuoi convertire?")
    bot.register_next_step_handler(sent_msg,convertmoney_step2, second )

def convertmoney_step2(message, second):
    many = message.text
    c = CurrencyConverter()
    example = c.convert(many, 'EUR', second)
    bot.send_message(message.chat.id, str(example))

bot.polling()