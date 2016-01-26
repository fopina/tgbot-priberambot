---
layout: index
---

xThis is a Telegram bot that will lookup up a portuguese word in [Priberam](http://priberam.pt), a portuguese dictionary.   Feel free to use it by talking to [@PriberamBot](http://telegram.me/priberambot).

[![Build Status](https://travis-ci.org/fopina/tgbot-buttiebot.svg?branch=master)](https://travis-ci.org/fopina/tgbot-buttiebot) [![Coverage Status](https://coveralls.io/repos/fopina/tgbot-priberambot/badge.svg?branch=master&service=github)](https://coveralls.io/github/fopina/tgbot-priberambot?branch=master)

PriberamBot was a developed using [TGBotPlug](http://fopina.github.io/tgbotplug).

This repository is ready for Heroku (as the bot is running there), so you can easily host your own:

* Register in [Heroku](https://www.heroku.com/)  
* Install and setup [heroku cli ](https://devcenter.heroku.com/articles/heroku-command), the command line tool  
* Talk to [@BotFather](http://telegram.me/botfather) to register your bot  
* And finally run these commands (replacing `<YOUR_APP_NAME>` for something of your choice and `<YOUR_BOT_TOKEN>` with the token provided by @BotFather)

    ```
    heroku create <YOUR_APP_NAME> --addons heroku-postgresql:hobby-dev
    heroku config:set TGTOKEN=<YOUR_BOT_TOKEN>
    heroku config:set MYAPPNAME=<YOUR_APP_NAME>
    heroku run './priberambot.py -d $DATABASE_URL --create_db'
    heroku ps:scale web=1
    ```

Have fun!
