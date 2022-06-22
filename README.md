# RetniNet
<img src="/images/logo.png" alt="RetniNet Logo" align="right" height="256px">
<div align="center">
  <h1>RetniNet</h1>
  <h3>A Telegram bot written in Python, totaly free and open-source.</h3>

![Repository Size](https://img.shields.io/github/repo-size/assenzostefano/retninet)
![Issues](https://img.shields.io/github/issues/assenzostefano/retninet)
![Pull Requests](https://img.shields.io/github/issues-pr/assenzostefano/retninet)
</div>

___
### Online on:
- [Telegram Bot](https://t.me/Retninet_bot)

___
### Installation and launching:
- Install **[Python](https://python.org)** on your machine. **Version 3.10 or higher is required!**
- Clone the repository on your machine.
- Open your console in the cloned repository.
- To complete the installation, write the following command in the console:
```console
pip install -r requirements.txt
```
- After installation, you will need to **[configure the bot](#bot-config)**.
- To start the bot, write the following command in the console:
```console
python index.py
```

___
### Bot config:

**DISCLAIMER: This bot must be used in educational purposes only. Your decisions are not our responsibility.**

- Create a bot on **[BotFather](https://t.me/BotFather)**.
- Go to the **Bot** tab, create a bot and copy its token.
- Create a file named **.env** or rename the **.env.example** file to **.env**.
- Open the **.env** file using any text editor.
- This file contains general bot settings in this format:

|       Field name        |               Example value                |                                Description                                     |
|:-----------------------:|:------------------------------------------:|:------------------------------------------------------------------------------:|
|         botToken        |                    "-"                     |  The token you copied from the BotFather, used to login the bot.        |
|         pastebinToken        |                    "-"                     |  Paste the Pastebin Token on the .env.example        |
|       weatherToken      |                         "-"                |  Paste the Weather Token on the .env.example   |
|         deeplToken         |            "-"            |              Paste the Deepl Token on the .env.example                 |
|         spotifyid         |            "-"            |              Paste the Spotify Id on the .env.example                 |
|         spotifysecret        |            "-"            |              Paste the Spotify Secret on the .env.example                 |
|         user_id       |            "-"            |              Paste your user id on the .env.example                 |
|         password        |            "-"            |              Paste the link for shutdown commands on the .env.example                 |
