<!-- PROJECT LOGO -->
  <br />
    <p align="center">
    <img src="Resources\logo.svg" alt="Logo" width="130" height="130">
  </a>
  <h1 align="center">Sentiment Analyzer</h1>
  <h2 align="center">The Bot is not active anymore</h2>
  <p align="center">
    You can still find the code, download it and try it for yourself.
  </p>
  <p align="center">
    A telegram bot that determines the polarity of a message using machine learning.
  </p>

[![Try it on telegram](https://img.shields.io/badge/try%20it-on%20telegram-0088cc.svg)](http://t.me/covid_sentiment_bot)
[![test](https://badgen.net/badge/License/GPL/green)](https://github.com/tiaringhio/Sentiment-Analyzer/blob/master/LICENSE)

## Table of contents

- [Table of contents](#table-of-contents)
- [About the project](#about-the-project)
- [First steps](#first-steps)
  - [Installation](#installation)
  - [Creating a bot](#creating-a-bot)
- [Usage](#usage)
  - [Polarity](#polarity)
  - [Wordcloud](#wordcloud)
- [License](#license)
- [Contributors](#contributors)

## About the project

This bot was to created as a proof of work of the classifier trained in this [Project](https://github.com/tiaringhio/COVID-19-Sentiments), it will analyze the polarity of a given message, answering with either positive or negative, the confidence of the prediciton and the polarity, for precision purposes. It uses the Logistic Regression Classifier. It's always online powered by a Raspberry Pi so it will not be as fast as it would be if it was running on a powerful computer, to make up for this you will se the bot either `typing...` or `uploading photo...`. It can even be added to groups!

## First steps

Here's a guide on getting started with the bot.

### Installation

Clone the repository then install the requirements using this command:

`$ pip3 install -r requirements.txt`

You should have all the packages needed to run the bot. If that's not the case just run `pip3 install package-name`

### Creating a bot

Contact the BotFather in Telegram (@botfather) and create the bot, it's pretty striaghtforward, you will need the API Token so copy it and paste it the `token.yaml` file inside the `""`:

<br />
    <p align="center">
    <img src="Resources\Screenshots\token info.png">

You can then run the bot with this command:

`$ python ./src/bot.py`

## Usage

These are the available commands:

- `/start` Starts the bot.
- `/predict` Analyze the incoming messages (default mode).
- `/wordcloud` Create a WordCloud based on the incoming messages, better suited for longer paragraphs.
- `/cancel` Stops the bot.

If the bot will not reiceve messages within 1 minute it will go to sleep and notify the user.

### Polarity

Command: `/predict`.

<sub>N.B. If you start the bot you dont'have to send the `/predict` command because it's the default state, you will need to use it to switch between functions. </sub>

It will analyze the text the user sends, answering with a positive, mixed or negative result, a degree of certainty (if the bot isn't sure about the result it will tell the user) and the polarity, for improved precision. Since this project has been made for the italian situation of COVID-19, it will analyze ialian text only.

<br />
    <p align="center">
    <img src="Resources\Screenshots\predict.png" width="500">

#### WordCloud

Command: `/wordcloud`.
Great for longer paragraphs of text, it will output a WordCloud.

<br />
    <p align="center">
    <img src="Resources\Screenshots\cloud1.png" width="500"><br />
    <p align="center">
    <img src="Resources\Screenshots\cloud2.png" width="500">

## License

Distributed under the GPL License. See `LICENSE` for more information.

Icons made by <a href="https://www.flaticon.com/authors/smashicons" title="Smashicons">Smashicons</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a>

## Contributors

[Mattia Ricci](https://github.com/tiaringhio) - 285237
